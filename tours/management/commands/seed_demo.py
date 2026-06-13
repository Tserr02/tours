from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand

from tours.models import Country, Hotel, Resort, Review, Tour, TourImage


COUNTRIES = {
    "turkey": {
        "name": "Турция",
        "short_description": "Пляжный отдых, семейные отели и насыщенная экскурсионная программа.",
        "description": "Турция подходит для семейного отдыха, поездок с детьми и коротких отпусков у моря.",
        "visa_requirements": "Для туристических поездок гражданам РФ обычно доступен безвизовый въезд на ограниченный срок.",
        "climate": "Средиземноморский климат: жаркое лето и мягкая весна.",
        "best_season": "Май - октябрь.",
        "attractions": "Античные города, Каппадокия, Памуккале, старый город Антальи.",
        "photo_url": "/static/img/country-turkey.jpg",
    },
    "egypt": {
        "name": "Египет",
        "short_description": "Красное море, дайвинг, отели all inclusive и экскурсии к древним памятникам.",
        "description": "Египет выбирают за теплое море, яркие коралловые рифы и стабильный пляжный сезон.",
        "visa_requirements": "Для въезда требуется туристическая виза, условия зависят от аэропорта прибытия.",
        "climate": "Сухой жаркий климат, комфортный для пляжного отдыха большую часть года.",
        "best_season": "Октябрь - май.",
        "attractions": "Пирамиды Гизы, Луксор, Каирский музей, коралловые рифы Шарм-эль-Шейха.",
        "photo_url": "/static/img/country-egypt.jpg",
    },
    "uae": {
        "name": "ОАЭ",
        "short_description": "Городской комфорт, пляжи, шопинг и высокий уровень сервиса.",
        "description": "ОАЭ подходят для отдыха у моря, деловых поездок и насыщенного городского досуга.",
        "visa_requirements": "Условия въезда зависят от гражданства и срока поездки.",
        "climate": "Жаркий пустынный климат, мягкая и сухая зима.",
        "best_season": "Ноябрь - март.",
        "attractions": "Бурдж-Халифа, Лувр Абу-Даби, пустынные сафари, набережные Дубая.",
        "photo_url": "/static/img/country-uae.jpg",
    },
    "greece": {
        "name": "Греция",
        "short_description": "Острова, белые города, античная история и чистое Эгейское море.",
        "description": "Греция сочетает пляжный отдых, прогулки по старым городам и экскурсии к памятникам античности.",
        "visa_requirements": "Для поездки обычно требуется шенгенская виза.",
        "climate": "Средиземноморский климат с сухим теплым летом и мягкой зимой.",
        "best_season": "Май - сентябрь.",
        "attractions": "Афины, Акрополь, Санторини, Крит, Метеоры, старые порты островов.",
        "photo_url": "/static/img/country-greece.jpg",
    },
    "thailand": {
        "name": "Таиланд",
        "short_description": "Тропические пляжи, острова, SPA, фрукты и яркая местная культура.",
        "description": "Таиланд подходит для пляжного отдыха, зимних поездок, островных маршрутов и семейных туров.",
        "visa_requirements": "Условия въезда зависят от срока поездки и гражданства туриста.",
        "climate": "Тропический климат с влажным сезоном и теплым морем круглый год.",
        "best_season": "Ноябрь - март.",
        "attractions": "Пхукет, Краби, Самуи, Бангкок, храмы, национальные парки и острова.",
        "photo_url": "/static/img/country-thailand.jpg",
    },
    "spain": {
        "name": "Испания",
        "short_description": "Средиземноморские пляжи, города, гастрономия и европейский сервис.",
        "description": "Испания подойдет для пляжного отдыха, экскурсий, семейных поездок и комбинированных маршрутов.",
        "visa_requirements": "Для поездки обычно требуется шенгенская виза.",
        "climate": "Мягкий средиземноморский климат на побережье и более сухой климат внутри страны.",
        "best_season": "Май - октябрь.",
        "attractions": "Барселона, Мадрид, Валенсия, Коста-Брава, Андалусия и исторические старые города.",
        "photo_url": "/static/img/country-spain.jpg",
    },
}


RESORTS = {
    "antalya": ("turkey", "Анталья", "Крупный курорт с пляжами, отелями и удобным аэропортом."),
    "sharm": ("egypt", "Шарм-эль-Шейх", "Популярный курорт Красного моря с рифами и бухтами."),
    "dubai": ("uae", "Дубай", "Современный мегаполис с пляжами, торговыми центрами и развлечениями."),
    "crete": ("greece", "Крит", "Большой греческий остров с пляжами, бухтами и древними дворцами."),
    "phuket": ("thailand", "Пхукет", "Тропический остров с пляжами, бухтами и насыщенной инфраструктурой."),
    "costa-brava": ("spain", "Коста-Брава", "Живописное побережье с пляжами, старыми городами и бухтами."),
}


COUNTRY_TOUR_VARIANTS = {
    "turkey": {
        "resort": "antalya",
        "hotel_names": [
            "Lara Family Resort",
            "Sun Aqua Palace",
            "Mediterranean SPA Hotel",
            "Sea View Lara Club",
        ],
        "items": [
            ("family-antalya-lara", "Семейный отдых в Анталье", 9, 2, 1, "UAI", "238000", "261000", "hot"),
            ("antalya-aqua-family", "Анталья с аквапарком", 7, 2, 2, "UAI", "221000", None, "available"),
            ("turkey-spa-week", "SPA-неделя на Средиземном море", 6, 2, 0, "AI", "184000", None, "available"),
            ("lara-sea-view", "Лара: номер с видом на море", 10, 2, 1, "UAI", "269000", "288000", "hot"),
        ],
    },
    "egypt": {
        "resort": "sharm",
        "hotel_names": [
            "Reef Bay Hotel",
            "Coral Garden Resort",
            "Family Bay Sharm",
            "Winter Sun Beach Hotel",
        ],
        "items": [
            ("reef-sharm-diving", "Красное море и домашний риф", 7, 2, 0, "AI", "176500", None, "available"),
            ("sharm-snorkeling-week", "Снорклинг в Шарм-эль-Шейхе", 8, 2, 0, "AI", "189000", "205000", "hot"),
            ("egypt-family-bay", "Семейная бухта Красного моря", 9, 2, 1, "AI", "214000", None, "available"),
            ("sharm-winter-sun", "Зимнее солнце Египта", 6, 2, 0, "HB", "152000", None, "available"),
        ],
    },
    "uae": {
        "resort": "dubai",
        "hotel_names": [
            "Marina Skyline Hotel",
            "Dubai Shopping Residence",
            "Palm Premium Suites",
            "Family Marina Resort",
        ],
        "items": [
            ("dubai-marina-city-break", "Дубай: пляж и город", 6, 2, 0, "BB", "289000", None, "available"),
            ("dubai-shopping-week", "Шопинг и пляжи Дубая", 5, 2, 0, "BB", "251000", None, "available"),
            ("uae-premium-weekend", "Премиум-уикенд в ОАЭ", 4, 2, 0, "BB", "228000", "247000", "hot"),
            ("dubai-family-marina", "Семейный Дубай у Марины", 7, 2, 1, "HB", "326000", None, "available"),
        ],
    },
    "greece": {
        "resort": "crete",
        "hotel_names": [
            "Aegean Blue Resort",
            "Santorini Light Hotel",
            "Crete Family Beach",
            "Antique Route Boutique",
        ],
        "items": [
            ("crete-aegean-blue", "Крит и Эгейское море", 7, 2, 0, "BB", "224000", None, "available"),
            ("greece-romantic-island", "Романтическая неделя в Греции", 6, 2, 0, "HB", "246000", "263000", "hot"),
            ("crete-family-beach", "Семейный пляжный Крит", 9, 2, 1, "HB", "278000", None, "available"),
            ("greece-antique-route", "Греция: море и античные маршруты", 8, 2, 0, "BB", "239000", None, "available"),
        ],
    },
    "thailand": {
        "resort": "phuket",
        "hotel_names": [
            "Lagoon Palm Resort",
            "Tropical Winter Villas",
            "Phuket Family Villa",
            "Thai Island Relax Hotel",
        ],
        "items": [
            ("phuket-lagoon-palm", "Пхукет: лагуна и пальмы", 10, 2, 0, "BB", "312000", None, "available"),
            ("thailand-tropical-winter", "Тропическая зима в Таиланде", 12, 2, 0, "BB", "348000", "371000", "hot"),
            ("phuket-family-villa", "Семейная вилла на Пхукете", 11, 2, 2, "HB", "426000", None, "available"),
            ("thai-island-relax", "Островной релакс в Таиланде", 8, 2, 0, "BB", "286000", None, "available"),
        ],
    },
    "spain": {
        "resort": "costa-brava",
        "hotel_names": [
            "Costa Brava Garden Hotel",
            "Mediterranean Family Coast",
            "Barcelona Beach Residence",
            "Brava Seaside Week Hotel",
        ],
        "items": [
            ("costa-brava-garden", "Коста-Брава у моря", 7, 2, 0, "BB", "198000", None, "available"),
            ("spain-family-coast", "Семейная Испания на побережье", 10, 2, 1, "HB", "256000", None, "available"),
            ("barcelona-and-beach", "Барселона и пляжный отдых", 6, 2, 0, "BB", "218000", "234000", "hot"),
            ("spain-mediterranean-week", "Средиземноморская неделя", 8, 2, 0, "HB", "229000", None, "available"),
        ],
    },
}


class Command(BaseCommand):
    help = "Создает демонстрационные страны, отели и туры."

    def handle(self, *args, **options):
        countries = {
            slug: Country.objects.update_or_create(slug=slug, defaults=data)[0]
            for slug, data in COUNTRIES.items()
        }

        resorts = {}
        for slug, (country_slug, name, description) in RESORTS.items():
            resorts[slug] = Resort.objects.update_or_create(
                country=countries[country_slug],
                name=name,
                defaults={"description": description},
            )[0]

        base_date = date.today() + timedelta(days=21)
        created_count = 0
        updated_count = 0

        hotel_stars = [5, 4, 5, 4]
        hotel_ratings = [Decimal("8.9"), Decimal("8.5"), Decimal("9.0"), Decimal("8.6")]

        for country_index, (country_slug, group) in enumerate(COUNTRY_TOUR_VARIANTS.items()):
            for tour_index, item in enumerate(group["items"]):
                slug, title, nights, adults, children, meal_type, price, old_price, status = item
                start_date = base_date + timedelta(days=country_index * 5 + tour_index * 7)
                hotel_name = group["hotel_names"][tour_index]
                hotel = Hotel.objects.update_or_create(
                    resort=resorts[group["resort"]],
                    name=hotel_name,
                    defaults={
                        "stars": hotel_stars[tour_index],
                        "rating": hotel_ratings[tour_index],
                        "description": (
                            f"{hotel_name} расположен на курорте {resorts[group['resort']].name} "
                            "и подходит для выбранного формата отдыха."
                        ),
                        "amenities": "Бассейн, ресторан, Wi-Fi, трансфер, экскурсионная поддержка, зона отдыха.",
                        "room_types": "Standard, Superior, Family Room.",
                        "photo_url": f"/static/img/hotel-{slug}.jpg",
                    },
                )[0]
                tour, created = Tour.objects.update_or_create(
                    slug=slug,
                    defaults={
                        "title": title,
                        "hotel": hotel,
                        "start_date": start_date,
                        "nights": nights,
                        "adults": adults,
                        "children": children,
                        "meal_type": meal_type,
                        "price": Decimal(price),
                        "old_price": Decimal(old_price) if old_price else None,
                        "description": (
                            f"{title}: пакетный тур с проживанием, перелетом, трансфером "
                            "и сопровождением менеджера туристической фирмы."
                        ),
                        "flight_info": "Перелет эконом-классом, багаж включен. Точное время уточняется при подтверждении заявки.",
                        "transfer_info": "Групповой трансфер аэропорт - отель - аэропорт включен в стоимость.",
                        "insurance_included": True,
                        "status": status,
                        "is_featured": tour_index == 0 or status == "hot",
                    },
                )
                created_count += int(created)
                updated_count += int(not created)

                tour.images.all().delete()
                TourImage.objects.create(tour=tour, image_url=hotel.photo_url, caption=title)

                Review.objects.get_or_create(
                    tour=tour,
                    author_name="Анна",
                    defaults={
                        "rating": 5,
                        "text": "Менеджер быстро подтвердил заявку, описание тура совпало с поездкой.",
                    },
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Демо-данные готовы. Стран: {len(COUNTRIES)}, туров: {sum(len(g['items']) for g in COUNTRY_TOUR_VARIANTS.values())}. "
                f"Создано: {created_count}, обновлено: {updated_count}."
            )
        )
