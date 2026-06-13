from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    BookingRequestForm,
    ProfileForm,
    RegistrationForm,
    ReviewForm,
    SubscriberForm,
    TourSearchForm,
    UserUpdateForm,
)
from .models import BookingRequest, ClientProfile, Country, Favorite, Review, Subscriber, Tour


def _filtered_tours(params):
    form = TourSearchForm(params or None)
    tours = Tour.objects.select_related("hotel__resort__country").prefetch_related("images")

    if form.is_valid():
        data = form.cleaned_data
        if data.get("country"):
            tours = tours.filter(hotel__resort__country=data["country"])
        if data.get("start_from"):
            tours = tours.filter(start_date__gte=data["start_from"])
        if data.get("start_to"):
            tours = tours.filter(start_date__lte=data["start_to"])
        if data.get("nights"):
            tours = tours.filter(nights=data["nights"])
        if data.get("adults"):
            tours = tours.filter(adults__gte=data["adults"])
        if data.get("children") is not None:
            tours = tours.filter(children__gte=data["children"])
        if data.get("meal_type"):
            tours = tours.filter(meal_type=data["meal_type"])
        if data.get("stars"):
            tours = tours.filter(hotel__stars=data["stars"])
        if data.get("min_price"):
            tours = tours.filter(price__gte=data["min_price"])
        if data.get("max_price"):
            tours = tours.filter(price__lte=data["max_price"])

        sort = data.get("sort")
        ordering = {
            "price": "price",
            "-price": "-price",
            "nights": "nights",
            "-rating": "-hotel__rating",
        }.get(sort)
        if ordering:
            tours = tours.order_by(ordering)

    return form, tours


def home(request):
    form, tours = _filtered_tours(request.GET)
    featured_tours = tours.filter(Q(is_featured=True) | Q(status="hot"))[:6]
    countries = Country.objects.annotate(tour_count=Count("resorts__hotels__tours"))[:6]
    subscriber_form = SubscriberForm()
    return render(
        request,
        "tours/home.html",
        {
            "form": form,
            "featured_tours": featured_tours,
            "countries": countries,
            "subscriber_form": subscriber_form,
        },
    )


def tour_list(request):
    form, tours = _filtered_tours(request.GET)
    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(request.user.favorites.values_list("tour_id", flat=True))
    return render(
        request,
        "tours/tour_list.html",
        {"form": form, "tours": tours, "favorite_ids": favorite_ids},
    )


def tour_detail(request, slug):
    tour = get_object_or_404(
        Tour.objects.select_related("hotel__resort__country").prefetch_related("images", "reviews"),
        slug=slug,
    )
    similar_tours = (
        Tour.objects.select_related("hotel__resort__country")
        .filter(hotel__resort__country=tour.country)
        .exclude(pk=tour.pk)[:3]
    )
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(user=request.user, tour=tour).exists()
    review_form = ReviewForm()
    return render(
        request,
        "tours/tour_detail.html",
        {
            "tour": tour,
            "similar_tours": similar_tours,
            "is_favorite": is_favorite,
            "review_form": review_form,
        },
    )


def countries(request):
    country_list = Country.objects.annotate(tour_count=Count("resorts__hotels__tours"))
    return render(request, "tours/countries.html", {"countries": country_list})


def country_detail(request, slug):
    country = get_object_or_404(Country.objects.prefetch_related("resorts__hotels"), slug=slug)
    tours = Tour.objects.select_related("hotel__resort").filter(hotel__resort__country=country)[:6]
    return render(request, "tours/country_detail.html", {"country": country, "tours": tours})


def booking_request(request, slug):
    tour = get_object_or_404(Tour, slug=slug)
    initial = {}
    if request.user.is_authenticated:
        profile, _ = ClientProfile.objects.get_or_create(user=request.user)
        initial = {
            "full_name": request.user.get_full_name(),
            "phone": profile.phone,
            "email": request.user.email,
        }

    if request.method == "POST":
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.tour = tour
            request_obj.user = request.user if request.user.is_authenticated else None
            request_obj.save()
            messages.success(request, "Заявка отправлена. Менеджер свяжется с вами в ближайшее время.")
            return redirect("tour_detail", slug=tour.slug)
    else:
        form = BookingRequestForm(initial=initial)

    return render(request, "tours/booking_form.html", {"form": form, "tour": tour})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация завершена.")
            return redirect("profile")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    profile_obj, _ = ClientProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Данные профиля сохранены.")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile_obj)

    bookings = BookingRequest.objects.filter(user=request.user).select_related("tour")[:10]
    return render(
        request,
        "tours/profile.html",
        {"user_form": user_form, "profile_form": profile_form, "bookings": bookings},
    )


@login_required
def favorites(request):
    items = Favorite.objects.select_related("tour__hotel__resort__country").filter(user=request.user)
    return render(request, "tours/favorites.html", {"favorites": items})


@login_required
@require_POST
def toggle_favorite(request, slug):
    tour = get_object_or_404(Tour, slug=slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, tour=tour)
    if created:
        messages.success(request, "Тур добавлен в избранное.")
    else:
        favorite.delete()
        messages.info(request, "Тур удален из избранного.")
    return redirect(request.POST.get("next") or tour.get_absolute_url())


@login_required
@require_POST
def add_review(request, slug):
    tour = get_object_or_404(Tour, slug=slug)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.tour = tour
        review.user = request.user
        review.author_name = request.user.get_full_name() or request.user.email
        review.save()
        messages.success(request, "Спасибо за отзыв.")
    else:
        messages.error(request, "Проверьте оценку и текст отзыва.")
    return redirect("tour_detail", slug=tour.slug)


@require_POST
def subscribe(request):
    form = SubscriberForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data["email"].lower()
        _, created = Subscriber.objects.get_or_create(email=email)
        if created:
            messages.success(request, "Вы успешно подписались на новости.")
        else:
            messages.info(request, "Этот email уже подписан.")
    else:
        messages.error(request, "Введите корректный email.")
    return redirect(request.POST.get("next") or "home")
