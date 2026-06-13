from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("tours/", views.tour_list, name="tour_list"),
    path("tours/<slug:slug>/", views.tour_detail, name="tour_detail"),
    path("tours/<slug:slug>/request/", views.booking_request, name="booking_request"),
    path("tours/<slug:slug>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("tours/<slug:slug>/review/", views.add_review, name="add_review"),
    path("countries/", views.countries, name="countries"),
    path("countries/<slug:slug>/", views.country_detail, name="country_detail"),
    path("profile/", views.profile, name="profile"),
    path("favorites/", views.favorites, name="favorites"),
    path("subscribe/", views.subscribe, name="subscribe"),
]
