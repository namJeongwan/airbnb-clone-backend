from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    RELATED_NAME = "photos"

    file = models.URLField()
    description = models.CharField(
        max_length=140,
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

    def __str__(self):
        return "Photo File"


class Video(CommonModel):
    RELATED_NAME = "Videos"

    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
    )

    def __str__(self):
        return "Video File"


