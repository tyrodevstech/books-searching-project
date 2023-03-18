from django.shortcuts import render, redirect, HttpResponse
from app_book.forms import CustomUserCreationForm, UserRegistrationForm, CustomUserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random

from app_book.models import User


# Create your views here.


def home_index(request):
    return render(request, 'home/index.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
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
            send_mail("OTP From Test System", message,
                      email_from, recipient_list)

            messages.success(request, 'Account Created successfully !')
            return redirect('app_book:registration')

    context = {
        'form': form,
    }
    return render(request, 'auth/registration.html', context)


@login_required(login_url='app_book:login')
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')
