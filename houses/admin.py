from django.contrib import admin
from .models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):

    fields = ("name", "address", ("price", "pets_allowed"))

    list_display = [
        "name",
        "price",
        "address",
        "pets_allowed",
    ]

    list_filter = ["price"]

    search_fields = ["name"]

    list_display_links = ["address", "name"]
