from django.db import models


# Create your models here.
class House(models.Model):
    """Model Definition for house"""
    name = models.CharField(max_length=140, help_text="House's name")
    price = models.PositiveIntegerField(help_text="1 night price")
    description = models.TextField()
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(default=True)

    def __str__(self):
        return self.name

