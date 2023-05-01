from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ("Profile",
         {
             "fields": (
                 "avatar",
                 "username",
                 "password",
                 "name",
                 "email",
                 "is_host",
                 "gender",
                 "language",
                 "currency",
             ),
         },
         ),
        ("Permissions",
         {
             "fields":
                 ("is_active",
                  "is_staff",
                  "is_superuser",
                  "groups",
                  "user_permissions",
                  ),
             "classes":
                 ("collapse",),
         },
         ),
        ("Important Dates",
         {
             "fields":
                 ("last_login",
                  "date_joined"
                  ),
             "classes":
                 ("collapse",),
         },
         ),
    )

    list_display = (
        "avatar",
        "email",
        "username",
        "is_host",
        "name",
    )

    list_display_links = [
        "name",
    ]
