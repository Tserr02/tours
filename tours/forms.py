from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import BookingRequest, ClientProfile, Country, Review, Subscriber, phone_validator


class TourSearchForm(forms.Form):
    country = forms.ModelChoiceField(
        label="Страна",
        required=False,
        queryset=Country.objects.none(),
        empty_label="Любая страна",
    )
    start_from = forms.DateField(label="Дата от", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    start_to = forms.DateField(label="Дата до", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    nights = forms.IntegerField(label="Ночей", required=False, min_value=1)
    adults = forms.IntegerField(label="Взрослых", required=False, min_value=1)
    children = forms.IntegerField(label="Детей", required=False, min_value=0)
    meal_type = forms.ChoiceField(
        label="Питание",
        required=False,
        choices=[("", "Любое"), ("RO", "Без питания"), ("BB", "Завтраки"), ("HB", "Полупансион"), ("FB", "Полный пансион"), ("AI", "Все включено"), ("UAI", "Ультра все включено")],
    )
    stars = forms.IntegerField(label="Звездность", required=False, min_value=1, max_value=5)
    min_price = forms.DecimalField(label="Цена от", required=False, min_value=0)
    max_price = forms.DecimalField(label="Цена до", required=False, min_value=0)
    sort = forms.ChoiceField(
        label="Сортировка",
        required=False,
        choices=[
            ("", "По умолчанию"),
            ("price", "Цена по возрастанию"),
            ("-price", "Цена по убыванию"),
            ("nights", "Длительность"),
            ("-rating", "Рейтинг отеля"),
        ],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["country"].queryset = Country.objects.order_by("name")


class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ["full_name", "phone", "email", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 4}),
        }


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=150)
    last_name = forms.CharField(label="Фамилия", max_length=150)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Телефон", validators=[phone_validator])
    personal_data = forms.BooleanField(label="Согласие на обработку персональных данных")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "password1", "password2", "personal_data"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"].lower()
        user.email = self.cleaned_data["email"].lower()
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            ClientProfile.objects.create(user=user, phone=self.cleaned_data["phone"])
        return user


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            "phone",
            "birth_date",
            "passport_series",
            "passport_number",
            "passport_issued_by",
            "passport_issue_date",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "passport_issue_date": forms.DateInput(attrs={"type": "date"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
        }


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]
