from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin: admin.ModelAdmin,
                 request: WSGIRequest,
                 queryset: QuerySet):
    for room in queryset:
        room.price = 0
        room.save()
