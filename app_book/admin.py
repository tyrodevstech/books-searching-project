from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app_book.models import *
from app_book.forms import CustomUserChangeForm, CustomUserCreationForm


admin.site.site_header = "Book Search Services"


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
        (
            None,
            {
                "fields": (
                    "email",
                    "name",
                    "password",
                    "phone",
                    "other_phone",
                    "role",
                    "otp",
                    "image",
                    "address",
                    "is_verified",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
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
                    "is_verified",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(StoreModel)
admin.site.register(ContactModel)
admin.site.register(ReviewModel)
admin.site.register(BookModel)
admin.site.register(BookCategoryModel)
admin.site.register(PublisherModel)
admin.site.register(AuthorModel)
admin.site.register(OrderModel)
admin.site.register(PaymentModel)
admin.site.register(BlogModel)
