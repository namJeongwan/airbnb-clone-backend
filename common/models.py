from django.db import models


# Create your models here.
class CommonModel(models.Model):
    """ Common Model Definition """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # DataBase 에 추가하지 않는 추상 모델
        abstract = True


