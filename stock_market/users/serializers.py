from rest_framework import serializers
from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
            "role",
            "image",
            "is_blocked",
            "balance",
            "subscriptions",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "role",
            "is_blocked",
            "balance",
            "subscriptions",
            "created_at",
            "updated_at",
        )

        extra_kwargs = {"password": {"write_only": True}}


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "role",
            "image",
            "is_blocked",
            "balance",
            "subscriptions",
            "created_at",
            "updated_at",
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "role",
            "image",
            "is_blocked",
            "balance",
            "subscriptions",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "email",
            "username",
            "role",
            "image",
            "created_at",
            "updated_at",
        )


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("subscriptions",)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=128, required=True, write_only=True)
    new_password = serializers.CharField(max_length=128, required=True, write_only=True)
    new_repeated_password = serializers.CharField(
        max_length=128, required=True, write_only=True
    )

    class Meta:
        model = User
        fields = ("old_password", "new_password", "new_repeated_password")

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_repeated_password"]:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match"}
            )

        return attrs

    def validate_old_password(self, password):
        user = self.context["request"].jwt_user
        if not user.check_password(password):
            raise serializers.ValidationError(
                {"old_password": "Old password is incorrect!"}
            )

        return password
