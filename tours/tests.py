from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import BookingRequest, Country, Hotel, Resort, Tour


class TourFlowTests(TestCase):
    def setUp(self):
        country = Country.objects.create(
            name="Турция",
            slug="turkey",
            short_description="Пляжный отдых",
            description="Популярное направление для семейного отдыха.",
        )
        resort = Resort.objects.create(country=country, name="Анталья")
        hotel = Hotel.objects.create(
            resort=resort,
            name="Lara Family Resort",
            stars=5,
            rating=Decimal("8.8"),
            description="Отель на первой линии.",
        )
        self.tour = Tour.objects.create(
            title="Семейный отдых в Анталье",
            slug="family-antalya-lara-test",
            hotel=hotel,
            start_date=date.today() + timedelta(days=10),
            nights=7,
            adults=2,
            children=1,
            meal_type="AI",
            price=Decimal("190000"),
            description="Тур с перелетом и трансфером.",
        )

    def test_catalog_filters_by_country(self):
        response = self.client.get(reverse("tour_list"), {"country": self.tour.country.id})
        self.assertContains(response, self.tour.title)

    def test_tour_detail_is_available(self):
        response = self.client.get(self.tour.get_absolute_url())
        self.assertContains(response, self.tour.hotel.name)

    def test_guest_can_create_booking_request(self):
        response = self.client.post(
            reverse("booking_request", kwargs={"slug": self.tour.slug}),
            {
                "full_name": "Иванов Иван Иванович",
                "phone": "+7 900 100-20-30",
                "email": "ivan@example.com",
                "comment": "Позвонить вечером",
            },
        )
        self.assertRedirects(response, self.tour.get_absolute_url())
        self.assertEqual(BookingRequest.objects.count(), 1)
