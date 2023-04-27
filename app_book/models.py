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
    role = models.CharField(
        max_length=122, choices=ROLE_TYPE, null=True, default=ROLE_TYPE[0][0]
    )
    otp = models.CharField(max_length=122, null=True, blank=True)
    image = models.ImageField(
        upload_to="profile_picture/%Y/%d/%b", null=True, blank=True
    )
    address = models.TextField(max_length=522, null=True, blank=True)
    is_verified = models.BooleanField(default=False, null=True)

    date = models.DateField(auto_now_add=True)

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"


class StoreModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='store')
    name = models.CharField(max_length=525, null=True, blank=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    street = models.TextField(max_length=525, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    licence = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=999, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"

    def __str__(self):
        return f"{self.name}"


class AuthorModel(models.Model):
    author_name = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return f"{self.author_name}"


class PublisherModel(models.Model):
    publisher_name = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return f"{self.publisher_name}"


class BookCategoryModel(models.Model):
    category_name = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return f"{self.category_name}"


class BookModel(models.Model):
    store = models.ForeignKey(
        StoreModel, on_delete=models.SET_NULL, null=True, blank=True,related_name='store_set'
    )
    title = models.CharField(max_length=225, null=True, blank=True)
    description = models.TextField(max_length=925, null=True, blank=True)
    cover_image = models.ImageField(
        upload_to="cover-image/%Y/%d/%b", null=True, blank=True
    )
    author = models.ForeignKey(
        AuthorModel, on_delete=models.SET_NULL, null=True, blank=True,related_name='author_set'
    )
    publisher = models.ForeignKey(
        PublisherModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    category = models.ForeignKey(
        BookCategoryModel, on_delete=models.SET_NULL, null=True, blank=True,related_name='category_set'
    )
    publication_date = models.DateField(default=timezone.now)
    price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class OrderModel(models.Model):
    ORDER_STATUS = (
        ("Pending", "Pending"),
        ("Complete", "Complete"),
        ("Cancelled", "Cancelled"),
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer_orders",
    )
    order_status = models.CharField(
        max_length=122, choices=ORDER_STATUS, null=True, default=ORDER_STATUS[0][0]
    )
    book = models.ForeignKey(
        BookModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    store = models.ForeignKey(
        StoreModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    seller = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="seller_orders",
    )
    is_paid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order-#{self.id}"


class ContactModel(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=20)
    message = models.TextField(max_length=255)

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class ReviewModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.CharField(max_length=500, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}"
