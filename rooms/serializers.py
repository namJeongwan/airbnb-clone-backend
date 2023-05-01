from rest_framework.serializers import ModelSerializer, SerializerMethodField

from categories.serializers import TinyCategorySerializer
from reviews.serializers import ReviewSerializer
from users.serializers import TinyUserSerializer
from medias.serializers import PhotoSerializer

from .models import Amenity, Room
from wishlists.models import Wishlist


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
    photos = PhotoSerializer(many=True, read_only=True)
    # reviews = ReviewSerializer(
    #     many=True,
    #     read_only=True,
    # )

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
            "photos",
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
    photos = PhotoSerializer(many=True, read_only=True)
    is_liked = SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        print(self.context)
        request = self.context.get('request')
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        if Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists():
            return "❤"
        else:
            return "🤍"

    def get_is_liked(self, room):
        request = self.context["request"]
        if Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists():
            return "❤"
        else:
            return "🤍"
