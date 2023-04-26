from rest_framework.serializers import ModelSerializer, SerializerMethodField

from categories.serializers import TinyCategorySerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class TinyAmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = [
            "name",
            "description",
        ]


class RoomListSerializer(ModelSerializer):
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
        ]

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        print(self.context)
        request = self.context.get('request')
        return room.owner == request.user


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    amenities = TinyAmenitySerializer(read_only=True, many=True)
    category = TinyCategorySerializer(read_only=True)
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        print(self.context)
        request = self.context.get('request')
        return room.owner == request.user
