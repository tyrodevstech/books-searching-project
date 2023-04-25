from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from app_book.forms import (
    CustomUserCreationForm,
    UserRegistrationForm,
    CustomUserChangeForm,
    UserUpdateForm,
    BookForm,
    BookCategoryForm,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import Http404

from app_book.models import User, BookModel, BookCategoryModel
from app_book.decorators import custom_dec


from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from django.urls import reverse_lazy

# Create your views here.


def home_index(request):
    return render(request, "home/index.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("app_book:dashboard")
    else:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            userObject = User.objects.filter(email=email).last()

            if userObject:
                eamil = userObject.email
            user = authenticate(email=eamil, password=password)
            if user is not None:
                login(request, user)
                return redirect("app_book:dashboard")
            else:
                print("error")
                messages.error(
                    request, "Email or Password didn't match. Please try again!"
                )
    return render(request, "auth/login.html")


@login_required(login_url="app_book:login")
def logout_view(request):
    logout(request)
    return redirect("app_book:login")


def registration_view(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            number = random.randint(1000, 9999)
            new_form = form.save(commit=False)
            new_form.otp = number
            new_form.save()

            message = f"Hi, {new_form.name}. This is your OTP: {number}. Please, verify your account."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [
                new_form.email,
            ]

            try:
                send_mail("OTP From Test System", message, email_from, recipient_list)
            except:
                print("Email is not valid!")

            messages.success(request, "Account Created successfully !")
            return redirect("app_book:registration")

    context = {
        "form": form,
    }
    return render(request, "auth/registration.html", context)


@login_required(login_url="app_book:login")
# @custom_dec
def dashboard_view(request):
    if not request.user.is_verified:
        user = get_object_or_404(User, id=request.user.id)

        if request.method == "POST":
            otp = request.POST.get("otp")

            if user.otp == otp:
                user.is_verified = True
                user.save()
                return redirect("app_book:dashboard")
            else:
                print("Didn't Matched!")
                messages.error(request, "OTP Didn't Matched!. Please try again!")

        return render(request, "dashboard/comfirm_account.html")
    else:
        return render(request, "dashboard/dashboard.html")


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "dashboard/update_profile.html"
    success_url = reverse_lazy("app_book:update_profile")
    def get_object(self, queryset=None):
        return self.request.user
    # def get_form_kwargs(self):
    #     print('test',self.request.user)
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'instance': self.request.user})
    #     return kwargs
    # def post(self, request, *args, **kwargs):
    #     """
    #     Handle POST requests: instantiate a form instance with the passed
    #     POST variables and then check if it's valid.
    #     """
    #     form = self.get_form()
    #     print(self.request.POST)

    #     if form.is_valid():
    #         print('form valid')
    #         form.save()
    #         return self.form_valid(form)
    #     else:
    #         print(form.errors)
    #         return self.form_invalid(form)


# Book
class BookBaseView(View):
    model = BookModel
    success_url = reverse_lazy("app_book:book_list")


class BookListView(BookBaseView, ListView):
    template_name = "dashboard/book/list.html"


class BookDetailView(BookBaseView, DetailView):
    template_name = "dashboard/book/details.html"


class BookCreateView(BookBaseView, CreateView):
    template_name = "dashboard/book/create.html"
    form_class = BookForm


class BookUpdateView(BookBaseView, UpdateView):
    template_name = "dashboard/book/edit.html"
    form_class = BookForm


class BookDeleteView(BookBaseView, DeleteView):
    template_name = "dashboard/book/delete.html"


# Book Categpry
class BookCategoryBaseView(View):
    model = BookCategoryModel
    success_url = reverse_lazy("app_book:book_category_list")


class BookCategoryListView(BookCategoryBaseView, ListView):
    template_name = "dashboard/category/list.html"


class BookCategoryCreateView(BookCategoryBaseView, CreateView):
    template_name = "dashboard/category/create.html"
    form_class = BookCategoryForm


class BookCategoryUpdateView(BookCategoryBaseView, UpdateView):
    template_name = "dashboard/category/edit.html"
    form_class = BookCategoryForm


class BookCategoryDeleteView(BookCategoryBaseView, DeleteView):
    template_name = "dashboard/category/delete.html"
