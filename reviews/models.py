from django.core.validators import MaxValueValidator
from django.db import models
from common.models import CommonModel

RELATED_NAME = "reviews"


class Review(CommonModel):
    """Review from a User to a Room or Experience"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
    )

    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
    )

    payload = models.TextField()

    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    def __str__(self) -> str:
        return f"{self.user} / {''.join(['★' for _ in range(0, self.rating)])}"
