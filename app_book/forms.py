from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from app_book.models import User, StoreModel, BookModel, BookCategoryModel
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
            "location",
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
            # 'image': forms.ImageField(),
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

        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name', 'required': 'required'}),
        # }


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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "Select Category"
        self.fields["author"].empty_label = "Select Author"
        self.fields["publisher"].empty_label = "Select Publisher"


class BookCategoryForm(forms.ModelForm):
    class Meta:
        model = BookCategoryModel
        fields = "__all__"

        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name', 'required': 'required'}),
        # }
