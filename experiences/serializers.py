from rest_framework.serializers import ModelSerializer

from users.serializers import TinyUserSerializer
from .models import Perk, Experience


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class TinyPerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = [
            "name",
            "details",
            "description",
        ]


class ExperienceListSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "name",
            "country",
            "city",
            "price",
            "address",
        ]


class ExperienceDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    perks = TinyPerkSerializer(read_only=True, many=True)

    class Meta:
        model = Experience
        fields = "__all__"