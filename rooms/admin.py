from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from .admin_action import *
from .models import Room, Amenity


# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "rating",
        "price",
        "kind",
        "total_amenities",
        "owner",
        "created_at",
    ]

    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "amenities",
        "toilets",
        "created_at",
        "updated_at",
    )

    search_fields = [
        "^name",
        "=price",
        "^owner__username",
    ]
    
    search_help_text = "원하는 키워드를 입력해보세요!"

    actions = [
        reset_prices,
    ]



@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )