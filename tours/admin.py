from django.contrib import admin

from .models import (
    BookingRequest,
    ClientProfile,
    Country,
    Favorite,
    Hotel,
    Resort,
    Review,
    Subscriber,
    Tour,
    TourImage,
)


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "best_season")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(Resort)
class ResortAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    list_filter = ("country",)
    search_fields = ("name",)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "resort", "stars", "rating")
    list_filter = ("stars", "resort__country")
    search_fields = ("name", "resort__name", "resort__country__name")


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("title", "hotel", "start_date", "nights", "meal_type", "price", "status", "is_featured")
    list_filter = ("status", "meal_type", "hotel__stars", "hotel__resort__country")
    list_editable = ("status", "is_featured")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "hotel__name", "hotel__resort__country__name")
    inlines = [TourImageInline]


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "tour", "phone", "email", "status", "created_at")
    list_filter = ("status", "created_at")
    list_editable = ("status",)
    search_fields = ("full_name", "phone", "email", "tour__title")
    date_hierarchy = "created_at"


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "birth_date")
    search_fields = ("user__first_name", "user__last_name", "user__email", "phone")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "tour", "created_at")
    search_fields = ("user__email", "tour__title")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author_name", "tour", "rating", "is_published", "created_at")
    list_filter = ("rating", "is_published")
    search_fields = ("author_name", "tour__title", "text")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)
