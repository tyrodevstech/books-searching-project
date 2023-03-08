from django.urls import path
from app_book.views import *

app_name = "app_book"

urlpatterns = [
    path("", home_index, name="text",),
]
