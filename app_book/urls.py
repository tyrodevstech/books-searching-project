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
    path(
        "book-category/list/", BookCategoryListView.as_view(), name="book_category_list"
    ),
    path(
        "book-category/create/",
        BookCategoryCreateView.as_view(),
        name="book_category_create",
    ),
    path(
        "book-category/edit/<int:pk>/",
        BookCategoryUpdateView.as_view(),
        name="book_category_edit",
    ),
    path(
        "book-category/delete/<int:pk>/",
        BookCategoryDeleteView.as_view(),
        name="book_category_delete",
    ),
    # book author
    path("book-author/list/", BookAuthorListView.as_view(), name="book_author_list"),
    path(
        "book-author/create/",
        BookAuthorCreateView.as_view(),
        name="book_author_create",
    ),
    path(
        "book-author/edit/<int:pk>/",
        BookAuthorUpdateView.as_view(),
        name="book_author_edit",
    ),
    path(
        "book-author/delete/<int:pk>/",
        BookAuthorDeleteView.as_view(),
        name="book_author_delete",
    ),
    # book publisher
    path(
        "book-publisher/list/",
        BookPublisherListView.as_view(),
        name="book_publisher_list",
    ),
    path(
        "book-publisher/create/",
        BookPublisherCreateView.as_view(),
        name="book_publisher_create",
    ),
    path(
        "book-publisher/edit/<int:pk>/",
        BookPublisherUpdateView.as_view(),
        name="book_publisher_edit",
    ),
    path(
        "book-publisher/delete/<int:pk>/",
        BookPublisherDeleteView.as_view(),
        name="book_publisher_delete",
    ),
    # order
    path(
        "order/list/",
        OrderListView.as_view(),
        name="order_list",
    ),
    path(
        "",
        home_index,
        name="home",
    ),
    path("store/", store_view, name="store"),
    path("review/add/", AddReview.as_view(), name="review"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("api/test/", search_book, name="test"),
]


htmx_urlpatters = [
    path("hx-search-list", search_list_view, name="hx_search_list"),
    path("search-details/<int:pk>", search_details_view, name="search_details"),
]
urlpatterns += htmx_urlpatters
