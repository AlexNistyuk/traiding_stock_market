from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        write_only_fields = ("password",)
        read_only_fields = (
            "is_blocked",
            "role",
            "created_at",
            "updated_at",
            "balance",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
        read_only_fields = (
            "email",
            "username",
            "role",
            "image",
            "created_at",
            "updated_at",
        )


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
        user = self.context["request"].user
        if not user.check_password(password):
            raise serializers.ValidationError(
                {"old_password": "Old password is incorrect!"}
            )

        return password
