import json
from abc import ABC

from django.contrib import admin


class WordFilter(admin.SimpleListFilter, ABC):
    title = "Filter by words!"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("bad", "Bad"),
            ("good", "Good"),
        ]

    def queryset(self, request, queryset):
        word = self.value()
        if word == "bad":
            return queryset.filter(rating__lt=3)
        elif word == "good":
            return queryset.filter(rating__gte=3)
        else:
            return queryset
