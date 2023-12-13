from decimal import Decimal

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator
from django.db import models


class Roles(models.TextChoices):
    ADMIN = ("admin", "admin")
    USER = ("user", "user")
    ANALYST = ("analyst", "analyst")


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not all([email, username, password]):
            raise ValueError(
                "User must have an email address, an username and a password"
            )

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, username, password):
        return self._create_user(
            email=email,
            username=username,
            password=password,
            role=Roles.USER,
        )

    def create_superuser(self, email, password, username):
        return self._create_user(
            email=email,
            username=username,
            password=password,
            role=Roles.ADMIN,
        )

    def create_analyst(self, email, password, username):
        return self._create_user(
            email=email,
            username=username,
            password=password,
            role=Roles.ANALYST,
        )


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, db_index=True, null=False, max_length=255)
    username = models.CharField(max_length=30, unique=True, db_index=True, null=False)
    password = models.CharField(null=False, max_length=128)
    role = models.CharField(choices=Roles.choices, default=Roles.USER, null=False)
    image = models.ImageField(upload_to="avatars/", blank=True)
    is_reset_password = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    balance = models.DecimalField(
        max_digits=settings.DECIMAL_MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_login = None

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.role == Roles.ADMIN

    class Meta:
        db_table = "user"
        constraints = [
            models.CheckConstraint(
                check=models.Q(balance__gte=Decimal("0")),
                name="user_balance_non_negative",
            ),
        ]

    def __str__(self):
        return self.username
