from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse


phone_validator = RegexValidator(
    regex=r"^\+?[0-9\s().-]{10,20}$",
    message="Введите корректный номер телефона.",
)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField("создано", auto_now_add=True)
    updated_at = models.DateTimeField("обновлено", auto_now=True)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField("страна", max_length=120, unique=True)
    slug = models.SlugField("адрес", max_length=140, unique=True)
    short_description = models.TextField("краткое описание")
    description = models.TextField("описание")
    visa_requirements = models.TextField("визовые требования", blank=True)
    climate = models.TextField("климат", blank=True)
    best_season = models.CharField("лучшее время", max_length=160, blank=True)
    attractions = models.TextField("достопримечательности", blank=True)
    photo_url = models.CharField("фото", max_length=255, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "страна"
        verbose_name_plural = "страны"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("country_detail", kwargs={"slug": self.slug})


class Resort(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="resorts", verbose_name="страна")
    name = models.CharField("курорт", max_length=120)
    description = models.TextField("описание", blank=True)

    class Meta:
        ordering = ["country__name", "name"]
        unique_together = ("country", "name")
        verbose_name = "курорт"
        verbose_name_plural = "курорты"

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class Hotel(models.Model):
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name="hotels", verbose_name="курорт")
    name = models.CharField("отель", max_length=160)
    stars = models.PositiveSmallIntegerField(
        "звезды",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    rating = models.DecimalField(
        "рейтинг",
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    description = models.TextField("описание")
    amenities = models.TextField("удобства", blank=True)
    room_types = models.TextField("типы номеров", blank=True)
    photo_url = models.CharField("фото", max_length=255, blank=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("resort", "name")
        verbose_name = "отель"
        verbose_name_plural = "отели"

    def __str__(self):
        return self.name


class Tour(TimeStampedModel):
    MEAL_CHOICES = [
        ("RO", "Без питания"),
        ("BB", "Завтраки"),
        ("HB", "Полупансион"),
        ("FB", "Полный пансион"),
        ("AI", "Все включено"),
        ("UAI", "Ультра все включено"),
    ]
    STATUS_CHOICES = [
        ("available", "Доступен"),
        ("hot", "Горящий тур"),
        ("sold_out", "Распродан"),
    ]

    title = models.CharField("название тура", max_length=180)
    slug = models.SlugField("адрес", max_length=200, unique=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, related_name="tours", verbose_name="отель")
    start_date = models.DateField("дата заезда")
    nights = models.PositiveSmallIntegerField("ночей", validators=[MinValueValidator(1), MaxValueValidator(60)])
    adults = models.PositiveSmallIntegerField("взрослых", default=2, validators=[MinValueValidator(1)])
    children = models.PositiveSmallIntegerField("детей", default=0)
    meal_type = models.CharField("питание", max_length=3, choices=MEAL_CHOICES)
    price = models.DecimalField("цена", max_digits=12, decimal_places=2)
    old_price = models.DecimalField("старая цена", max_digits=12, decimal_places=2, null=True, blank=True)
    description = models.TextField("описание тура")
    flight_info = models.TextField("перелет", blank=True)
    transfer_info = models.TextField("трансфер", blank=True)
    insurance_included = models.BooleanField("страховка включена", default=True)
    status = models.CharField("статус", max_length=20, choices=STATUS_CHOICES, default="available")
    is_featured = models.BooleanField("на главной", default=False)

    class Meta:
        ordering = ["start_date", "price"]
        verbose_name = "тур"
        verbose_name_plural = "туры"

    def __str__(self):
        return self.title

    @property
    def country(self):
        return self.hotel.resort.country

    @property
    def resort(self):
        return self.hotel.resort

    def get_absolute_url(self):
        return reverse("tour_detail", kwargs={"slug": self.slug})


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="images", verbose_name="тур")
    image_url = models.CharField("изображение", max_length=255)
    caption = models.CharField("подпись", max_length=160, blank=True)

    class Meta:
        verbose_name = "изображение тура"
        verbose_name_plural = "изображения туров"

    def __str__(self):
        return self.caption or self.tour.title


class ClientProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField("телефон", max_length=32, blank=True, validators=[phone_validator])
    birth_date = models.DateField("дата рождения", null=True, blank=True)
    passport_series = models.CharField("серия паспорта", max_length=12, blank=True)
    passport_number = models.CharField("номер паспорта", max_length=20, blank=True)
    passport_issued_by = models.CharField("кем выдан", max_length=255, blank=True)
    passport_issue_date = models.DateField("дата выдачи", null=True, blank=True)

    class Meta:
        verbose_name = "профиль клиента"
        verbose_name_plural = "профили клиентов"

    def __str__(self):
        return self.user.get_full_name() or self.user.email or self.user.username


class BookingRequest(TimeStampedModel):
    STATUS_CHOICES = [
        ("new", "Новая"),
        ("confirmed", "Подтверждена"),
        ("paid", "Оплачена"),
        ("cancelled", "Отменена"),
    ]

    tour = models.ForeignKey(Tour, on_delete=models.PROTECT, related_name="booking_requests", verbose_name="тур")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="booking_requests",
        verbose_name="клиент",
        null=True,
        blank=True,
    )
    full_name = models.CharField("ФИО", max_length=180)
    phone = models.CharField("телефон", max_length=32, validators=[phone_validator])
    email = models.EmailField("email")
    comment = models.TextField("комментарий", blank=True)
    status = models.CharField("статус", max_length=20, choices=STATUS_CHOICES, default="new")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "заявка"
        verbose_name_plural = "заявки"

    def __str__(self):
        return f"{self.full_name}: {self.tour.title}"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField("добавлено", auto_now_add=True)

    class Meta:
        unique_together = ("user", "tour")
        ordering = ["-created_at"]
        verbose_name = "избранное"
        verbose_name_plural = "избранное"

    def __str__(self):
        return f"{self.user} -> {self.tour}"


class Review(TimeStampedModel):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="reviews", verbose_name="тур")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    author_name = models.CharField("имя", max_length=120)
    rating = models.PositiveSmallIntegerField(
        "оценка",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField("отзыв")
    is_published = models.BooleanField("опубликован", default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"

    def __str__(self):
        return f"{self.author_name}: {self.rating}/5"


class Subscriber(models.Model):
    email = models.EmailField("email", unique=True)
    created_at = models.DateTimeField("дата подписки", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "подписчик"
        verbose_name_plural = "подписчики"

    def __str__(self):
        return self.email
