from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from app_book.models import (
    User,
    StoreModel,
    BookModel,
    BookCategoryModel,
    ReviewModel,
    ContactModel,
    AuthorModel,
    PublisherModel,
    OrderModel,
)
from django.utils.translation import gettext_lazy as _

from django.forms.widgets import ClearableFileInput


class CustomImageFieldWidget(ClearableFileInput):
    clear_checkbox_label = _("Clear")
    initial_text = _("Currently")
    input_text = _("Change")
    template_name = "django/forms/widgets/custom_clearable_file_input.html"


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
        # fields = ("email",)


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "phone",
            "other_phone",
            "image",
            "address",
        )

        widgets = {
            "address": forms.Textarea(
                attrs={
                    "rows": "8",
                    "cols": "40",
                    "placeholder": "Write your address...",
                }
            ),
            "image": CustomImageFieldWidget,
        }


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "phone",
            "other_phone",
            "role",
            "password1",
            "password2",
            "image",
            "address",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your Name",
                    "required": "required",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "example@example.com"}
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your Phone",
                    "required": "required",
                }
            ),
            "other_phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your Other Phone"}
            ),
            "role": forms.Select(
                attrs={"class": "form-control", "required": "required"}
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "4",
                    "cols": "40",
                    "placeholder": "Your Address",
                    "style": "height: 100px !important;",
                    "required": "required",
                }
            ),
        }


class StoreForm(forms.ModelForm):
    class Meta:
        model = StoreModel
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                    "placeholder": "Your Store Name",
                    "required": "required",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                    "placeholder": "example@example.com",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                    "placeholder": "Your Phone Number",
                    "required": "required",
                }
            ),
            "street": forms.Textarea(
                attrs={
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                    "rows": "4",
                    "placeholder": "your street address...",
                    "required": "required",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                    "placeholder": "Your City Name",
                    "required": "required",
                }
            ),
            "zip_code": forms.NumberInput(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                    "placeholder": "Your Zip Code",
                    "required": "required",
                }
            ),
            "licence": forms.TextInput(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                    "placeholder": "Your Licence",
                    "required": "required",
                }
            ),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = "__all__"

        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                    "rows": "4",
                    "placeholder": "Leave your comments...",
                    "required": "required",
                }
            ),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "", "placeholder": "Name", "required": "required"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "", "placeholder": "Email", "required": "required"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "", "placeholder": "Phone", "required": "required"}
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "message-box",
                    "placeholder": "Leave a message...",
                    "required": "required",
                    "rows": 6,
                }
            ),
        }


class BookForm(forms.ModelForm):
    publication_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = BookModel
        fields = "__all__"

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Write a book description here...",
                    "rows": "8",
                }
            ),
            "cover_image": CustomImageFieldWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "Select Category"
        self.fields["author"].empty_label = "Select Author"
        self.fields["publisher"].empty_label = "Select Publisher"


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ["order_status", "is_paid", "book"]


class BookCategoryForm(forms.ModelForm):
    class Meta:
        model = BookCategoryModel
        fields = "__all__"

        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name', 'required': 'required'}),
        # }


class BookAuthorForm(forms.ModelForm):
    class Meta:
        model = AuthorModel
        fields = "__all__"


class BookPublisherForm(forms.ModelForm):
    class Meta:
        model = PublisherModel
        fields = "__all__"
