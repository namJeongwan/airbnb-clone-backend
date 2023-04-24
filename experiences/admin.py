from django.contrib import admin
from .models import Experience, Perk


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "price",
        "address",
        "start",
        "end",
    ]

    list_filter = [
        "price",
        "perks",
        "name",
        "address",
        "start",
        "end",
        "category",
    ]


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    pass
