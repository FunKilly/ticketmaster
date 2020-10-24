from django.contrib.auth import get_user_model
from rest_framework import serializers

from .exceptions import PasswordConfirmationFailedException
from .validators import validate_password

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ["email", "password", "password2", "name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = UserModel(
            email=self.validated_data["email"], name=self.validated_data["name"],
        )
        user.set_password(self.validated_data["password"])
        user.save()
        return user

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            raise PasswordConfirmationFailedException
        else:
            validate_password(password)
            return data


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
