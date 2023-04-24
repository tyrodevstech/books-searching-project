from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from django.utils import timezone


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
    is_verified = models.BooleanField(default=False, null=True)

    date = models.DateField(auto_now_add=True)

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"#{self.id}: {self.email}"


class StoreModel(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=525, null=True, blank=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True, region='BD')
    email = models.EmailField(null=True, blank=True, unique=True)
    street = models.TextField(max_length=525, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    licence = models.CharField(max_length=100, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Store")
        verbose_name_plural = ("Stores")

    def __str__(self):
        return f"Store: {self.name}"


class AuthorModel(models.Model):
    name = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return f"Store Name: {self.name}"


class PublisherModel(models.Model):
    publisher_name = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return f"Store Name: {self.title}"


class BookCategoryModel(models.Model):
    category_name = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return f"Category Name: {self.category_name}"


class BookModel(models.Model):
    title = models.CharField(max_length=225, null=True, blank=True)
    sub_title = models.CharField(max_length=525, null=True, blank=True)
    description = models.CharField(max_length=925, null=True, blank=True)
    cover_image = models.ImageField(
        upload_to="cover-image/%Y/%d/%b", null=True, blank=True)
    author = models.ForeignKey(
        AuthorModel, on_delete=models.SET_NULL, null=True, blank=True)
    publisher = models.ForeignKey(
        PublisherModel, on_delete=models.SET_NULL, null=True, blank=True)

    publication_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Store Name: {self.title}"


class StockModel(models.Model):
    store = models.ForeignKey(
        StoreModel, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(
        BookModel, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Store Name: {self.id}"


class ContactModel(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=20)
    message = models.TextField(max_length=255)

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Consumer Name: {self.name}"


class ReviewModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.CharField(max_length=500, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_at}'
