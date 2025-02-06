import factory
from factory.django import DjangoModelFactory
from users.models import User


class UserFactory(DjangoModelFactory):
    email = factory.Faker("email")
    username = factory.Faker("user_name")
    password = factory.Faker("password")
    image = factory.django.ImageField(filename="test.png")

    class Meta:
        model = User
