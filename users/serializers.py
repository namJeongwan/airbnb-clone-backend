from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from rooms.models import Room

from .models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "name",
            "avatar",
            "username",
            "is_host",
        ]


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        ]


class PublicUserSerializer(ModelSerializer):
    rooms = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "name",
            "gender",
            "language",
            "rooms",
        ]

    def get_rooms(self, user):
        print(user, type(user))
        rooms = Room.objects.filter(owner=user)
        rooms = [room.name for room in rooms]
        return rooms
