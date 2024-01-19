import random

import folium
import folium.plugins as plugs
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from geopy.distance import geodesic

from app_book.decorators import seller_decorator, user_decorator
from app_book.forms import (
    BookAuthorForm,
    BookCategoryForm,
    BookForm,
    BookPublisherForm,
    ContactForm,
    OrderForm,
    ReviewForm,
    StoreForm,
    UserRegistrationForm,
    UserUpdateForm,
)
from app_book.models import (
    AuthorModel,
    BlogModel,
    BookCategoryModel,
    BookModel,
    ContactModel,
    OrderModel,
    PaymentModel,
    PublisherModel,
    ReviewModel,
    StoreModel,
    User,
)

from .utils import getSortedBooksLocations
import uuid

# Create your views here.
seller_decorators = [login_required(login_url="app_book:login"), seller_decorator]
user_decorators = [login_required(login_url="app_book:login"), user_decorator]


class Home(FormView):
    template_name = "home/index.html"
    form_class = ContactForm
    success_url = reverse_lazy("app_book:home")

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Message Sent successfully !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blogs"] = BlogModel.objects.all()[:3]
        context["reviews"] = ReviewModel.objects.all()[:3]
        return context


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
        if request.user.role == "User":
            store_qs = StoreModel.objects.all()
            user_location = request.GET.get("user_location")

            if user_location:
                user_location_coords = tuple(map(float, user_location.split(",")))

                m = folium.Map(user_location_coords, zoom_start=11)

                # for store in store_qs:
                #     if store.location:
                #         store_location_coords = tuple(map(float, store.location.split(",")))
                #         folium.Marker(
                #             location=store_location_coords,
                #             tooltip="Click me!",
                #             popup=store.name,
                #             icon=folium.Icon(icon="store", color="blue", prefix="fa"),
                #         ).add_to(m)

                folium.Marker(
                    location=user_location_coords,
                    tooltip="Click me!",
                    popup="Me",
                    icon=folium.Icon(icon="user", color="red", prefix="fa"),
                ).add_to(m)

                context = {
                    "map": m._repr_html_(),
                }
            else:
                context = {
                    "map": None,
                }
            return render(request, "dashboard/user_dashboard.html", context)
        else:
            total_review = ReviewModel.objects.all().count()
            total_added_books = BookModel.objects.filter(
                store__user=request.user
            ).count()

            reviews = ReviewModel.objects.all().order_by("-id")[:5]

            context = {
                "total_review": total_review,
                "total_added_books": total_added_books,
                "reviews": reviews,
            }
            return render(request, "dashboard/seller_dashboard.html", context)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "dashboard/update_profile.html"
    success_url = reverse_lazy("app_book:update_profile")

    def get_object(self, queryset=None):
        return self.request.user


# Book
class BookBaseView(View):
    model = BookModel
    success_url = reverse_lazy("app_book:book_list")


@method_decorator(seller_decorators, name="dispatch")
class BookListView(BookBaseView, ListView):
    template_name = "dashboard/book/list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search_value", "")
        if search:
            queryset = queryset.filter(
                store__user=self.request.user, title__icontains=search
            )
        else:
            queryset = queryset.filter(store__user=self.request.user)

        return queryset


@method_decorator(seller_decorators, name="dispatch")
class BookDetailView(BookBaseView, DetailView):
    template_name = "dashboard/book/details.html"


@method_decorator(seller_decorators, name="dispatch")
class BookCreateView(BookBaseView, CreateView):
    template_name = "dashboard/book/create.html"
    form_class = BookForm

    def post(self, request, *args, **kwargs):
        has_store = hasattr(request.user, "store")
        form = self.get_form()
        if has_store:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            messages.success(request, "Create Store first!!")
            return redirect("app_book:store")

    def form_valid(self, form):
        new_form = form.save(commit=False)
        new_form.store = self.request.user.store
        self.object = new_form.save()
        return super().form_valid(form)


@method_decorator(seller_decorators, name="dispatch")
class BookUpdateView(BookBaseView, UpdateView):
    template_name = "dashboard/book/edit.html"
    form_class = BookForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        has_store = hasattr(request.user, "store")
        if has_store:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            messages.success(request, "Create Store first!!")
            return redirect("app_book:store")

    def form_valid(self, form):
        new_form = form.save(commit=False)
        new_form.store = self.request.user.store
        self.object = new_form.save()
        return super().form_valid(form)


@method_decorator(seller_decorators, name="dispatch")
class BookDeleteView(BookBaseView, DeleteView):
    template_name = "dashboard/book/delete.html"


# Book Categpry
class BookCategoryBaseView(View):
    model = BookCategoryModel
    success_url = reverse_lazy("app_book:book_category_list")


class BookCategoryListView(BookCategoryBaseView, ListView):
    template_name = "dashboard/category/list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if "search_value" in self.request.GET:
            search = self.request.GET.get("search_value", "")
            queryset = queryset.filter(category_name__icontains=search)
        return queryset


@method_decorator(seller_decorators, name="dispatch")
class BookCategoryCreateView(BookCategoryBaseView, CreateView):
    template_name = "dashboard/category/create.html"
    form_class = BookCategoryForm


@method_decorator(seller_decorators, name="dispatch")
class BookCategoryUpdateView(BookCategoryBaseView, UpdateView):
    template_name = "dashboard/category/edit.html"
    form_class = BookCategoryForm


@method_decorator(seller_decorators, name="dispatch")
class BookCategoryDeleteView(BookCategoryBaseView, DeleteView):
    template_name = "dashboard/category/delete.html"


# Author
class BookAuthorBaseView(View):
    model = AuthorModel
    success_url = reverse_lazy("app_book:book_author_list")


@method_decorator(seller_decorators, name="dispatch")
class BookAuthorListView(BookAuthorBaseView, ListView):
    template_name = "dashboard/author/list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if "search_value" in self.request.GET:
            search = self.request.GET.get("search_value", "")
            queryset = queryset.filter(author_name__icontains=search)
        return queryset


@method_decorator(seller_decorators, name="dispatch")
class BookAuthorCreateView(BookAuthorBaseView, CreateView):
    template_name = "dashboard/author/create.html"
    form_class = BookAuthorForm


@method_decorator(seller_decorators, name="dispatch")
class BookAuthorUpdateView(BookAuthorBaseView, UpdateView):
    template_name = "dashboard/author/edit.html"
    form_class = BookAuthorForm


@method_decorator(seller_decorators, name="dispatch")
class BookAuthorDeleteView(BookAuthorBaseView, DeleteView):
    template_name = "dashboard/author/delete.html"


# Publisher
class BookPublisherBaseView(View):
    model = PublisherModel
    success_url = reverse_lazy("app_book:book_publisher_list")


@method_decorator(seller_decorators, name="dispatch")
class BookPublisherListView(BookPublisherBaseView, ListView):
    template_name = "dashboard/publisher/list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if "search_value" in self.request.GET:
            search = self.request.GET.get("search_value", "")
            queryset = queryset.filter(publisher_name__icontains=search)
        return queryset


@method_decorator(seller_decorators, name="dispatch")
class BookPublisherCreateView(BookPublisherBaseView, CreateView):
    template_name = "dashboard/publisher/create.html"
    form_class = BookPublisherForm


@method_decorator(seller_decorators, name="dispatch")
class BookPublisherUpdateView(BookPublisherBaseView, UpdateView):
    template_name = "dashboard/publisher/edit.html"
    form_class = BookPublisherForm


@method_decorator(seller_decorators, name="dispatch")
class BookPublisherDeleteView(BookPublisherBaseView, DeleteView):
    template_name = "dashboard/publisher/delete.html"


@login_required(login_url="app_book:login")
@seller_decorator
def store_view(request):
    user = get_object_or_404(User, id=request.user.id)
    has_instance = hasattr(request.user, "store")

    if has_instance:
        store_obj = get_object_or_404(StoreModel, user=user)
        form = StoreForm(instance=store_obj)
    else:
        form = StoreForm()

    if request.method == "POST":
        if has_instance:
            form = StoreForm(request.POST, instance=store_obj)
        else:
            form = StoreForm(request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.save()

            if has_instance:
                messages.success(request, "Store Updated successfully !")
            else:
                messages.success(request, "Store Created successfully !")

            return redirect("app_book:store")

    context = {"form": form}
    return render(request, "dashboard/store.html", context)


@method_decorator(user_decorators, name="dispatch")
class AddReview(CreateView):
    model = ReviewModel
    success_url = "/dashboard/"
    form_class = ReviewForm
    template_name = "dashboard/review.html"

    def form_valid(self, form):
        new_form = form.save(commit=False)
        new_form.user = self.request.user
        self.object = new_form.save()
        messages.success(self.request, "Review Added successfully !")
        return super().form_valid(form)


class ContactView(CreateView):
    model = ContactModel
    success_url = "/contact/"
    form_class = ContactForm
    template_name = "home/contact.html"

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Message Sent successfully !")
        return super().form_valid(form)


class OrderBaseView(View):
    model = OrderModel
    success_url = reverse_lazy("app_book:order_list")


class OrderListView(OrderBaseView, ListView):
    template_name = "dashboard/order/list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search_value", "")

        if self.request.user.role == "Shop Owner":
            if search:
                return queryset.filter(
                    seller=self.request.user,
                    book__title__icontains=search,
                )
            else:
                return queryset.filter(seller=self.request.user)
        elif self.request.user.role == "User":
            if search:
                return queryset.filter(
                    customer=self.request.user,
                    book__title__icontains=search,
                )
            else:
                return queryset.filter(customer=self.request.user)
        else:
            return queryset


class CheckoutView(FormView):
    template_name = "dashboard/checkout.html"
    model = OrderModel
    form_class = OrderForm

    def get_success_url(self):
        return reverse_lazy(
            "app_book:payment",
            kwargs={
                "pk": self.order.id,
            },
        )

    def form_valid(self, form):
        order = form.save(commit=False)

        quantity = self.get_context_data().get("quantity")
        book = self.get_context_data().get("book")

        order.book = book
        order.store = book.store
        order.customer = self.request.user
        order.seller = book.store.user
        order.books_quantity = quantity
        order.order_status = "Complete"
        order.is_paid = True
        order.save()
        self.order = order
        messages.success(self.request, "Order placed successfully !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        book_id = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        quantity = int(self.request.GET.get("quantity", 1))
        book = get_object_or_404(BookModel, id=book_id)
        context["book"] = book
        context["quantity"] = quantity
        context["price"] = book.price
        context["sub_total_price"] = round(book.price * quantity, 2)
        context["total_price"] = round((book.price * quantity) + 70, 2)
        return context


class OrderDetailsView(OrderBaseView, DetailView):
    template_name = "dashboard/order/details.html"
    context_object_name = "order_obj"

    def get_context_data(self, **kwargs):
        order_id = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(OrderModel, id=order_id)

        context["sub_total_price"] = round(order.book.price * order.books_quantity, 2)
        context["total_price"] = round(
            (order.book.price * order.books_quantity) + 70, 2
        )
        return context


class PaymentView(TemplateView):
    template_name = "dashboard/payment.html"
    success_url = reverse_lazy("app_book:dashboard")

    def get(self, request, pk, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        order = get_object_or_404(OrderModel, pk=pk)
        if not hasattr(order, "payment"):
            payment = PaymentModel()
            payment.order = order
            payment.amount_paid = (order.books_quantity * order.book.price) + 70
            payment.transaction_id = str(uuid.uuid4())
            payment.save()
            order.is_paid
        print(order.payment)
        return self.render_to_response(context)


@method_decorator(seller_decorators, name="dispatch")
class OrderUpdateView(OrderBaseView, UpdateView):
    template_name = "dashboard/order/edit.html"
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer"] = self.get_object().customer.email
        return context


@method_decorator(seller_decorators, name="dispatch")
class OrderDeleteView(OrderBaseView, DeleteView):
    template_name = "dashboard/order/delete.html"


from django.db.models import Count


@login_required(login_url="app_book:login")
@user_decorator
def book_search_list_view(request):
    search_text = request.POST.get("query")

    if search_text:
        results = (
            BookModel.objects.filter(
                Q(title__icontains=search_text)
                | Q(author__author_name__icontains=search_text)
                | Q(publisher__publisher_name__icontains=search_text)
                | Q(category__category_name__icontains=search_text)
            )
            .select_related("store", "author")
            .values("title", "author__author_name", "category__category_name")
            .annotate(count=Count("title"))
            .order_by("title")[:12]
        )
        context = {
            "searched_books": results,
        }
        return render(request, "partials/book-search-results.html", context)
    else:
        return HttpResponse("")


@login_required(login_url="app_book:login")
@user_decorator
def available_store_list_view(request):
    book_title = request.POST.get("title")
    user_location = request.POST.get("location")

    if book_title:
        book_qs = BookModel.objects.filter(title__icontains=book_title)[:10]
        sorted_books = getSortedBooksLocations(user_location, book_qs)

        context = {
            "sorted_books": sorted_books,
            "user_location": user_location,
        }
        return render(request, "partials/available-book-stores.html", context)
    else:
        return HttpResponse("")


@login_required(login_url="app_book:login")
@user_decorator
def search_details_view(request, pk):
    book = get_object_or_404(BookModel, id=pk)
    user_location = request.GET.get("user_location")
    store_location = book.store.location

    if store_location and user_location:
        user_location_coords = tuple(map(float, user_location.split(",")))
        store_location_coords = tuple(map(float, store_location.split(",")))

        m = folium.Map(user_location_coords, zoom_start=11)

        folium.Marker(
            location=user_location_coords,
            tooltip="Click me!",
            popup="Me",
            icon=folium.Icon(icon="user", color="red", prefix="fa"),
        ).add_to(m)

        folium.Marker(
            location=store_location_coords,
            popup=book.store.name,
            icon=folium.Icon(icon="store", color="blue", prefix="fa"),
        ).add_to(m)

        distance = round(
            geodesic(user_location_coords, store_location_coords).kilometers, 2
        )

        line = folium.PolyLine(
            [store_location_coords, user_location_coords],
            weight=3,
            tooltip=f"Distance: {distance}km",
        ).add_to(m)
        attr = {"fill": "#000", "font-weight": "bold", "font-size": "14"}
        wind_textpath = plugs.PolyLineTextPath(
            line, f"{distance}km", center=True, offset=20, attributes=attr
        )
        m.add_child(line)
        m.add_child(wind_textpath)

        context = {
            "book": book,
            "map": m._repr_html_(),
        }
    else:
        context = {
            "book": book,
            "map": None,
        }

    return render(request, "dashboard/search_details.html", context)


@login_required(login_url="app_book:login")
@user_decorator
def stores_map_view(request):
    store_qs = StoreModel.objects.all()
    user_location = request.GET.get("user_location")

    if user_location:
        user_location_coords = tuple(map(float, user_location.split(",")))

        m = folium.Map(user_location_coords, zoom_start=11)

        for store in store_qs:
            if store.location:
                store_location_coords = tuple(map(float, store.location.split(",")))
                folium.Marker(
                    location=store_location_coords,
                    tooltip="Click me!",
                    popup=store.name,
                    icon=folium.Icon(icon="store", color="blue", prefix="fa"),
                ).add_to(m)

        folium.Marker(
            location=user_location_coords,
            tooltip="Click me!",
            popup="Me",
            icon=folium.Icon(icon="user", color="red", prefix="fa"),
        ).add_to(m)

        context = {
            "map": m._repr_html_(),
        }
    else:
        context = {
            "map": None,
        }

    return render(request, "dashboard/map_view.html", context)


@login_required(login_url="app_book:login")
@user_decorator
def available_book_stores_map_view(request):
    book_title = request.POST.get("title")
    user_location = request.POST.get("location")
    if book_title and user_location:
        book_qs = BookModel.objects.filter(title__icontains=book_title)[:12]
        sorted_book_stores = getSortedBooksLocations(user_location, book_qs)

        user_location_coords = tuple(map(float, user_location.split(",")))

        m = folium.Map(user_location_coords, zoom_start=11)
        if sorted_book_stores:
            for store in sorted_book_stores:
                if store["store_location"]:
                    store_location_coords = tuple(
                        map(float, store["store_location"].split(","))
                    )
                    folium.Marker(
                        location=store_location_coords,
                        tooltip="Click me!",
                        popup=store["store_name"],
                        icon=folium.Icon(icon="store", color="blue", prefix="fa"),
                    ).add_to(m)
                    line = folium.PolyLine(
                        [store_location_coords, user_location_coords],
                        weight=3,
                        tooltip=f"Distance: {store['distance']}km",
                    ).add_to(m)
                    attr = {"fill": "#000", "font-weight": "bold", "font-size": "14"}
                    wind_textpath = plugs.PolyLineTextPath(
                        line,
                        f"{store['distance']}km",
                        center=True,
                        offset=20,
                        attributes=attr,
                    )
                    m.add_child(line)
                    m.add_child(wind_textpath)

        folium.Marker(
            location=user_location_coords,
            tooltip="Click me!",
            popup="Me",
            icon=folium.Icon(icon="user", color="red", prefix="fa"),
        ).add_to(m)

        return HttpResponse(m._repr_html_())
    else:
        return HttpResponse("")


def custom_page_not_found_view(request, exception=None):
    return render(request, "404.html", {})
