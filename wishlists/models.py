from django.db import models
from common.models import CommonModel

RELATED_NAME = "wishlists"


class Wishlist(CommonModel):
    """WishList Model Definition"""
    name = models.CharField(
        max_length=150,
    )
    rooms = models.ManyToManyField(
        "rooms.Room",
        related_name=RELATED_NAME,
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
        related_name=RELATED_NAME,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
    )

    def __str__(self) -> str:
        return self.name