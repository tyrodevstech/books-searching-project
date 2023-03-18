from django.db import models
from django.contrib.auth.models import AbstractUser

from app_book.manager import UserManager


# Create your models here.
class User(AbstractUser):
    ROLE_TYPE = (
        ("User", "User"),
        ("Shop Owner", "Shop Owner"),
    )
    name = models.CharField(max_length=122, null=True, blank=True)
    email = models.EmailField(("email address"), blank=True, unique=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    other_phone = models.CharField(max_length=12, null=True, blank=True)
    role = models.CharField(max_length=122, choices=ROLE_TYPE,
                            null=True, default=ROLE_TYPE[0][0])
    otp = models.CharField(max_length=122, null=True, blank=True)
    image = models.ImageField(
        upload_to="profile_picture/%Y/%d/%b", null=True, blank=True)
    address = models.TextField(max_length=522, null=True, blank=True)
    location = models.CharField(max_length=999, null=True, blank=True)
    active = models.BooleanField(default=False, null=True)
    date = models.DateField(auto_now_add=True)

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"#{self.id}: {self.email}"
