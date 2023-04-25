from django.urls import path
from app_book.views import *

app_name = "app_book"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("registration/", registration_view, name="registration"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("update-profile/", UserUpdateView.as_view(), name="update_profile"),
    # book
    path("book/list/", BookListView.as_view(), name="book_list"),
    path("book/create/", BookCreateView.as_view(), name="book_create"),
    path("book/edit/<int:pk>/", BookUpdateView.as_view(), name="book_edit"),
    path("book/details/<int:pk>/", BookDetailView.as_view(), name="book_details"),
    path("book/delete/<int:pk>/", BookDeleteView.as_view(), name="book_delete"),
    # book category
    path("book-category/list/", BookCategoryListView.as_view(), name="book_category_list"),
    path("book-category/create/", BookCategoryCreateView.as_view(), name="book_category_create"),
    path("book-category/edit/<int:pk>/", BookCategoryUpdateView.as_view(), name="book_category_edit"),
    path("book-category/delete/<int:pk>/", BookCategoryDeleteView.as_view(), name="book_category_delete"),

    path("", home_index, name="home",),
]
