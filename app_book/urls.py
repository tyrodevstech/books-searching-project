from django.urls import path
from app_book.views import *

app_name = "app_book"

urlpatterns = [
    path("", home_index, name="home",),

    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("registration/", registration_view, name="registration"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("update-profile/", update_profile_view, name="update_profile"),
]
