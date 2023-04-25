from rest_framework.serializers import ModelSerializer

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
    class Meta:
        model = Room
        fields = [
            "pk",
            "name",
            "country",
            "city",
            "price",
        ]


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    amenities = TinyAmenitySerializer(many=True)
    category = TinyCategorySerializer()

    class Meta:
        model = Room
        fields = "__all__"
