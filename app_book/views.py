from django.shortcuts import render, redirect, HttpResponse
from app_book.forms import CustomUserCreationForm, UserRegistrationForm, CustomUserChangeForm
from django.contrib import messages

# Create your views here.


def home_index(request):
    return render(request, 'home/index.html')


def login_view(request):
    return render(request, 'registration/login.html')


def registration_view(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created successfully !')
            return redirect('app_book:registration')

    context = {
        'form': form,
    }
    return render(request, 'registration/registration.html', context)


def dashboard_view(request):
    return HttpResponse("Dashboard Page!")
