from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from app_book.models import User, StoreModel


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'phone',
            'other_phone',
            'role',
            'password1',
            'password2',
            'image',
            'address',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone', 'required': 'required'}),
            'other_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Other Phone'}),
            'role': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            # 'image': forms.ImageField(),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'cols': '40', 'placeholder': 'Your Address', 'style': 'height: 100px !important;', 'required': 'required'}),
        }


class StoreForm(forms.ModelForm):
    class Meta:
        model = StoreModel
        fields = "__all__"

        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name', 'required': 'required'}),
        # }
