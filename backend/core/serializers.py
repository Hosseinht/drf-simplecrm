from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer


class UserSerializer(BaseUserSerializer):
    is_organizer = serializers.BooleanField()
    is_agent = serializers.BooleanField()

    def validate(self, data):
        if data["is_organizer"] and data["is_agent"]:
            raise serializers.ValidationError(
                "User can't be Agent and Organizer at the same time"
            )
        return data

    class Meta(BaseUserSerializer.Meta):
        # model = settings.AUTH_USER_MODEL
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_organizer",
            "is_agent",
        ]


class UserCreateSerializer(BaseUserCreateSerializer):
    is_organizer = serializers.BooleanField()
    is_agent = serializers.BooleanField()

    def validate(self, data):
        if data["is_organizer"] and data["is_agent"]:
            raise serializers.ValidationError(
                "User can't be Agent and Organizer at the same time"
            )
        return data

    class Meta(BaseUserCreateSerializer.Meta):
        # model = settings.AUTH_USER_MODEL
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_organizer",
            "is_agent",
        ]
