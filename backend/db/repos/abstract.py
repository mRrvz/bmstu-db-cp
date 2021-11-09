""" Abstract Class of Repository """

from abc import ABC, abstractmethod


class AbstractRepo(ABC):
    @abstractmethod
    def save(self, model):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, model_id):
        raise NotImplementedError

    @abstractmethod
    def get_by_filter(self, filter, keys):
        raise NotImplementedError

    @abstractmethod
    def get_objects_count_by_filter(self, filter, keys):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def remove(self, model_id):
        raise NotImplementedError

    @abstractmethod
    def edit(self, *args, **kwargs):
        raise NotImplementedError
