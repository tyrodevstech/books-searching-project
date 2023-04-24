from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random

from app_book.models import User, StoreModel, ReviewModel
from app_book.decorators import custom_dec
from app_book.forms import CustomUserCreationForm, UserRegistrationForm, CustomUserChangeForm, StoreForm, ReviewForm


# Create your views here.

def home_index(request):
    return render(request, 'home/index.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('app_book:dashboard')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            userObject = User.objects.filter(email=email).last()

            if userObject:
                eamil = userObject.email
            user = authenticate(email=eamil, password=password)
            if user is not None:
                login(request, user)
                return redirect('app_book:dashboard')
            else:
                print('error')
                messages.error(
                    request, "Email or Password didn't match. Please try again!")
    return render(request, 'auth/login.html')


@login_required(login_url='app_book:login')
def logout_view(request):
    logout(request)
    return redirect('app_book:login')


def registration_view(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            number = random.randint(1000, 9999)
            new_form = form.save(commit=False)
            new_form.otp = number
            new_form.save()

            message = f'Hi, {new_form.name}. This is your OTP: {number}. Please, verify your account.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [new_form.email, ]

            try:
                send_mail("OTP From Test System", message,
                          email_from, recipient_list)
            except:
                print("Email is not valid!")

            messages.success(request, 'Account Created successfully !')
            return redirect('app_book:registration')

    context = {
        'form': form,
    }
    return render(request, 'auth/registration.html', context)


@login_required(login_url='app_book:login')
# @custom_dec
def dashboard_view(request):
    if not request.user.is_verified:
        user = get_object_or_404(User, id=request.user.id)

        if request.method == 'POST':
            otp = request.POST.get('otp')

            if user.otp == otp:
                user.is_verified = True
                user.save()
                return redirect('app_book:dashboard')
            else:
                print("Didn't Matched!")
                messages.error(
                    request, "OTP Didn't Matched!. Please try again!")

        return render(request, 'dashboard/comfirm_account.html')
    else:
        return render(request, 'dashboard/dashboard.html')


@login_required(login_url='app_book:login')
def update_profile_view(request):
    return render(request, 'dashboard/update_profile.html')


@login_required(login_url='app_book:login')
def store_view(request):
    user = get_object_or_404(User, id=request.user.id)
    has_instance = hasattr(request.user, 'storemodel')

    if has_instance:
        store_obj = get_object_or_404(StoreModel, user=user)
        form = StoreForm(instance=store_obj)
    else:
        form = StoreForm()

    if request.method == 'POST':
        if has_instance:
            form = StoreForm(request.POST, instance=store_obj)
        else:
            form = StoreForm(request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.save()

            if has_instance:
                messages.success(request, 'Store Updated successfully !')
            else:
                messages.success(request, 'Store Created successfully !')

            return redirect('app_book:add_store')

    context = {
        "form": form
    }
    return render(request, 'dashboard/store.html', context)


class AddReview(CreateView):
    model = ReviewModel
    success_url = "/dashboard/"
    form_class = ReviewForm
    template_name = "dashboard/review.html"

    def form_valid(self, form):
        new_form = form.save(commit=False)
        new_form.user = self.request.user
        self.object = new_form.save()
        messages.success(self.request, 'Review Added successfully !')
        return super().form_valid(form)
