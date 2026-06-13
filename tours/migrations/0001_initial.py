# Generated for the course project scaffold.
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True, verbose_name="страна")),
                ("slug", models.SlugField(max_length=140, unique=True, verbose_name="адрес")),
                ("short_description", models.TextField(verbose_name="краткое описание")),
                ("description", models.TextField(verbose_name="описание")),
                ("visa_requirements", models.TextField(blank=True, verbose_name="визовые требования")),
                ("climate", models.TextField(blank=True, verbose_name="климат")),
                ("best_season", models.CharField(blank=True, max_length=160, verbose_name="лучшее время")),
                ("attractions", models.TextField(blank=True, verbose_name="достопримечательности")),
                ("photo_url", models.URLField(blank=True, verbose_name="фото")),
            ],
            options={"verbose_name": "страна", "verbose_name_plural": "страны", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Subscriber",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(max_length=254, unique=True, verbose_name="email")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="дата подписки")),
            ],
            options={"verbose_name": "подписчик", "verbose_name_plural": "подписчики", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="ClientProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="обновлено")),
                ("phone", models.CharField(blank=True, max_length=32, validators=[django.core.validators.RegexValidator(message="Введите корректный номер телефона.", regex="^\\+?[0-9\\s().-]{10,20}$")], verbose_name="телефон")),
                ("birth_date", models.DateField(blank=True, null=True, verbose_name="дата рождения")),
                ("passport_series", models.CharField(blank=True, max_length=12, verbose_name="серия паспорта")),
                ("passport_number", models.CharField(blank=True, max_length=20, verbose_name="номер паспорта")),
                ("passport_issued_by", models.CharField(blank=True, max_length=255, verbose_name="кем выдан")),
                ("passport_issue_date", models.DateField(blank=True, null=True, verbose_name="дата выдачи")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "профиль клиента", "verbose_name_plural": "профили клиентов"},
        ),
        migrations.CreateModel(
            name="Resort",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="курорт")),
                ("description", models.TextField(blank=True, verbose_name="описание")),
                ("country", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="resorts", to="tours.country", verbose_name="страна")),
            ],
            options={
                "verbose_name": "курорт",
                "verbose_name_plural": "курорты",
                "ordering": ["country__name", "name"],
                "unique_together": {("country", "name")},
            },
        ),
        migrations.CreateModel(
            name="Hotel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160, verbose_name="отель")),
                ("stars", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name="звезды")),
                ("rating", models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name="рейтинг")),
                ("description", models.TextField(verbose_name="описание")),
                ("amenities", models.TextField(blank=True, verbose_name="удобства")),
                ("room_types", models.TextField(blank=True, verbose_name="типы номеров")),
                ("photo_url", models.URLField(blank=True, verbose_name="фото")),
                ("resort", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="hotels", to="tours.resort", verbose_name="курорт")),
            ],
            options={
                "verbose_name": "отель",
                "verbose_name_plural": "отели",
                "ordering": ["name"],
                "unique_together": {("resort", "name")},
            },
        ),
        migrations.CreateModel(
            name="Tour",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="обновлено")),
                ("title", models.CharField(max_length=180, verbose_name="название тура")),
                ("slug", models.SlugField(max_length=200, unique=True, verbose_name="адрес")),
                ("start_date", models.DateField(verbose_name="дата заезда")),
                ("nights", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(60)], verbose_name="ночей")),
                ("adults", models.PositiveSmallIntegerField(default=2, validators=[django.core.validators.MinValueValidator(1)], verbose_name="взрослых")),
                ("children", models.PositiveSmallIntegerField(default=0, verbose_name="детей")),
                ("meal_type", models.CharField(choices=[("RO", "Без питания"), ("BB", "Завтраки"), ("HB", "Полупансион"), ("FB", "Полный пансион"), ("AI", "Все включено"), ("UAI", "Ультра все включено")], max_length=3, verbose_name="питание")),
                ("price", models.DecimalField(decimal_places=2, max_digits=12, verbose_name="цена")),
                ("old_price", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name="старая цена")),
                ("description", models.TextField(verbose_name="описание тура")),
                ("flight_info", models.TextField(blank=True, verbose_name="перелет")),
                ("transfer_info", models.TextField(blank=True, verbose_name="трансфер")),
                ("insurance_included", models.BooleanField(default=True, verbose_name="страховка включена")),
                ("status", models.CharField(choices=[("available", "Доступен"), ("hot", "Горящий тур"), ("sold_out", "Распродан")], default="available", max_length=20, verbose_name="статус")),
                ("is_featured", models.BooleanField(default=False, verbose_name="на главной")),
                ("hotel", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="tours", to="tours.hotel", verbose_name="отель")),
            ],
            options={"verbose_name": "тур", "verbose_name_plural": "туры", "ordering": ["start_date", "price"]},
        ),
        migrations.CreateModel(
            name="BookingRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="обновлено")),
                ("full_name", models.CharField(max_length=180, verbose_name="ФИО")),
                ("phone", models.CharField(max_length=32, validators=[django.core.validators.RegexValidator(message="Введите корректный номер телефона.", regex="^\\+?[0-9\\s().-]{10,20}$")], verbose_name="телефон")),
                ("email", models.EmailField(max_length=254, verbose_name="email")),
                ("comment", models.TextField(blank=True, verbose_name="комментарий")),
                ("status", models.CharField(choices=[("new", "Новая"), ("confirmed", "Подтверждена"), ("paid", "Оплачена"), ("cancelled", "Отменена")], default="new", max_length=20, verbose_name="статус")),
                ("tour", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="booking_requests", to="tours.tour", verbose_name="тур")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="booking_requests", to=settings.AUTH_USER_MODEL, verbose_name="клиент")),
            ],
            options={"verbose_name": "заявка", "verbose_name_plural": "заявки", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="добавлено")),
                ("tour", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorites", to="tours.tour")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorites", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "избранное",
                "verbose_name_plural": "избранное",
                "ordering": ["-created_at"],
                "unique_together": {("user", "tour")},
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="обновлено")),
                ("author_name", models.CharField(max_length=120, verbose_name="имя")),
                ("rating", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name="оценка")),
                ("text", models.TextField(verbose_name="отзыв")),
                ("is_published", models.BooleanField(default=True, verbose_name="опубликован")),
                ("tour", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="tours.tour", verbose_name="тур")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "отзыв", "verbose_name_plural": "отзывы", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="TourImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image_url", models.URLField(verbose_name="изображение")),
                ("caption", models.CharField(blank=True, max_length=160, verbose_name="подпись")),
                ("tour", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="tours.tour", verbose_name="тур")),
            ],
            options={"verbose_name": "изображение тура", "verbose_name_plural": "изображения туров"},
        ),
    ]
