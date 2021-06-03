""" Module to cache data via Tarantool and Time Queue """

import logging

from datetime import datetime
from heapq import heappush as insert_queue, heappop as extract_maximum

class CacheLRU():
    def __init__(self, max_size=100):
        self.max_size = max_size
        self.current_size = None
        self.time_queue = []

    def get(self, key, repo):
        current_time = datetime.timestamp(datetime.now())
        if self.current_size is None:
            self.current_size = self.get_cache_size(repo["tarantool"].connection)

        cached_object = repo["tarantool"].get_by_id(key)
        if cached_object is not None:
            logging.error("Cached")
            insert_queue(self.time_queue, (current_time, key))
            return cached_object

        logging.error("Not cahced")
        if self.current_size >= self.max_size:
            key = extract_maximum(self.time_queue)[-1]
            repo["tarantool"].remove(key)

        obj = repo["postgres"].get_by_id(key)
        repo["tarantool"].save(obj)
        insert_queue(self.time_queue, (current_time, key))
        self.increment_cache_size(repo["tarantool"].connection)

        return obj

    def insert(self, key, obj, repo):
        current_time = datetime.timestamp(datetime.now())

        if self.current_size is None:
            self.current_size = self.get_cache_size(repo.connection)

        if self.current_size >= self.max_size:
            key = extract_maximum(self.time_queue)[-1]
            repo.remove(key)

        insert_queue(self.time_queue, (current_time, key))
        self.increment_cache_size(repo.connection)
        repo.save(obj)

    def remove(self, key, repo):
        if self.current_size is None:
            self.current_size = self.get_cache_size(repo.connection)

        self.time_queue = list(filter(lambda x: x[1] != key, self.time_queue))
        self.decrement_cache_size(repo.connection)
        repo.remove(key)

    def update(self, key, repo):
        obj = self.remove(key, repo)
        self.insert(key, obj, repo)

    def increment_cache_size(self, connection):
        self.current_size += 1
        connection.space('cache_size').update(1, [('+', 1, 1)])

    def decrement_cache_size(self, connection):
        self.current_size += 1
        connection.space('cache_size').update(1, [('-', 1, 1)])

    def get_cache_size(self, connection):
        return connection.space('cache_size').select()[0][1]
