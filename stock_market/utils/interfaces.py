import abc


class IService(abc.ABC):
    """Interface for models services which provides db operations"""

    @abc.abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id_or_404(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def bulk_create(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def bulk_update(self, *args, **kwargs):
        raise NotImplementedError
