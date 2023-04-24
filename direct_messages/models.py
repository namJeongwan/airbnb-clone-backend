from django.db import models
from common.models import CommonModel


class ChattingRoom(CommonModel):
    """Room Model Definition"""
    RELATED_NAME = "chatting_rooms"

    users = models.ManyToManyField(
        "users.User",
        related_name=RELATED_NAME,
    )

    def __str__(self):
        return "Chatting Room."


class Message(CommonModel):
    """Message Model Definition"""
    RELATED_NAME = "message"
    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name=RELATED_NAME,
    )
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
    )

    def __str__(self):
        return f"{self.user} says: {self.text}"
