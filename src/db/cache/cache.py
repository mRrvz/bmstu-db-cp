""" Module to cache data via Tarantool and Time Queue """

import logging

from datetime import datetime
from heapq import heappush as insert_queue, heappop as extract_maximum

from db.utils import Utils

class CacheLRU():
    def __init__(self, max_size=100):
        self.max_size = max_size
        self.current_size = None
        self.time_queue = []

    def get_by_primary(self, key, space_name, repos):
        current_time = datetime.timestamp(datetime.now())
        cache_repo = repos["cache"][space_name]
        storage_repo = repos["storage"][space_name]

        if self.current_size is None:
            self.current_size = self.get_cache_size(cache_repo.connection)

        cached_object = cache_repo.get_by_id(key)
        if cached_object is not None:
            insert_queue(self.time_queue, (current_time, key, space_name))
            return cached_object

        if self.current_size >= self.max_size:
            min_key, cached_space_name = extract_maximum(self.time_queue)[1:]
            cache_repo.remove(min_key)
            self.decrement_cache_size(cache_repo.connection)

        obj = storage_repo.get_by_id(key)
        cache_repo.save(obj)
        self.increment_cache_size(cache_repo.connection)
        insert_queue(self.time_queue, (current_time, key, space_name))

        return obj

    def get_by_filter(self, space_name, key, index, repos):
        current_time = datetime.timestamp(datetime.now())
        cache_repo = repos["cache"][space_name]
        storage_repo = repos["storage"][space_name]

        if self.current_size is None:
            self.current_size = self.get_cache_size(cache_repo.connection)

        cached_objects, primary_keys = cache_repo.get_by_filter(index, key)
        if cached_objects is not None:
            for obj, primary_key in zip(cached_objects, primary_keys):
                insert_queue(self.time_queue, (current_time, primary_key, space_name))

        total_cnt = storage_repo.get_objects_count_by_filter(index, key)
        objects_left = total_cnt if cached_objects is None else total_cnt - len(cached_objects)
        if objects_left == 0:
            return cached_objects

        if objects_left == total_cnt:
            primary_keys = [-1] # Full-scan confirmed

        while self.current_size + objects_left >= self.max_size:
            min_key, space_name = extract_maximum(self.time_queue)[1:]
            repos["cache"][space_name].remove(min_key)
            self.decrement_cache_size(cache_repo.connection)

        filter_str = Utils.get_noncached_filter_string(len(primary_keys), index)
        objects, primary_keys = storage_repo.get_by_filter(filter_str, tuple(map(int, [key] + primary_keys)))

        for obj, primary_key in zip(objects, primary_keys):
            cache_repo.save(obj)
            self.increment_cache_size(cache_repo.connection)
            insert_queue(self.time_queue, (datetime.timestamp(datetime.now()), primary_key, space_name))

        return objects

    def insert(self, key, obj, repo):
        current_time = datetime.timestamp(datetime.now())

        if self.current_size is None:
            self.current_size = self.get_cache_size(repo.connection)

        if self.current_size >= self.max_size:
            key = extract_maximum(self.time_queue)[-1]
            repo.remove(key)

        insert_queue(self.time_queue, (current_time, key, repo._meta["space_name"]))
        self.increment_cache_size(repo.connection)
        repo.save(obj)

    def remove(self, key, space_name, repo):
        if self.current_size is None:
            self.current_size = self.get_cache_size(repo.connection)

        if repo.remove(key) is not None:
            self.time_queue = list(filter(lambda x: x[1] != key or x[2] != space_name, self.time_queue))
            self.decrement_cache_size(repo.connection)

    def update(self, key, repo):
        obj = self.remove(key, repo)
        self.insert(key, obj, repo)

    def clear(self, repos, connection):
        for key in repos:
            space_name = repos[key]._meta["space_name"]
            connection.call(f"box.space.{space_name}:truncate", ())

        connection.space("cache_size").replace((1, 0))

    def increment_cache_size(self, connection):
        self.current_size += 1
        connection.space("cache_size").replace((1, self.current_size))

    def decrement_cache_size(self, connection):
        self.current_size -= 1
        connection.space("cache_size").replace((1, self.current_size))

    def get_cache_size(self, connection):
        return connection.space("cache_size").select()[0][1]
