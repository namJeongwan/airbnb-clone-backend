from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.template.defaultfilters import default


class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        # (value, label)
        MALE = ("male", "남")
        FEMALE = ("female", "여")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "한국어")
        EN = ("en", "영어")
        
    class CurrencyChoices(models.TextChoices):
        WON = ("won", "원")
        USD = ("usd", "달러")

    first_name = models.CharField(
        max_length=150,
        editable=False
    )
    last_name = models.CharField(
        max_length=150,
        editable=False
    )
    avatar = models.ImageField(blank=True)
    name = models.CharField(
        max_length=150,
        default="",
        verbose_name="당신의 이름"
    )

    is_host = models.BooleanField(
        default=False
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )

    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )

    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )