from django.urls import path
from app_book.views import *

app_name = "app_book"

urlpatterns = [
    path("", home_index, name="home",),

    path("login/", login_view, name="login"),
    path("registration/", registration_view, name="registration"),
    path("dashboard/", dashboard_view, name="dashboard"),
]
