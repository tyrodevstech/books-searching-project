from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app_book.models import User
from app_book.forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        "name",
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "name",
        "phone",
        "name",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": (
            "email",
            "name",
            "password",
            "phone",
            "other_phone",
            "role",
            "otp",
            "image",
            "address",
            "location",
            "is_verified",
        )}),
        ("Permissions", {"fields": (
            "is_staff",
            "is_active",
            "groups",
            "user_permissions"
        )}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "name",
                "phone",
                "other_phone",
                "role",
                "otp",
                "image",
                "address",
                "location",
                "is_verified",
                "password1",
                "password2",
                "is_staff",
                "is_active",
                "groups",
                "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
