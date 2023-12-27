import abc

from django.http import Http404
from users.exceptions import Http400
from users.models import User


class IService(abc.ABC):
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


class UserService(IService):
    def __init__(self, validated_data: dict = None, instance: User = None):
        self.data = validated_data
        self.instance = instance

    def create(self):
        return User.objects.create_user(**self.data)

    def update(self):
        try:
            self.instance.is_blocked = self.data["is_blocked"]
            self.instance.balance = self.data["balance"]
            self.instance.subscriptions.set(self.data["subscriptions"])
            self.instance.save()

            return self.instance
        except KeyError as exc:
            raise Http400({"detail": [f"{exc} is not provided"]})

    def get_by_id_or_404(self, user_id: int):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

    def delete(self, user: User):
        return user.delete()

    def get_all(self):
        return User.objects.all()

    def bulk_create(self, users: list[User]):
        return User.objects.bulk_create(users)

    def bulk_update(self, users: list[User]):
        return User.objects.bulk_update(users)

    def change_password(self, user):
        user.set_password(self.data["new_password"])
        user.save()

    def set_subscriptions(self, user):
        try:
            user.subscriptions.set(self.data["subscriptions"])
            user.save()
        except KeyError:
            raise Http400({"detail": "'subscriptions' is not provided"})
