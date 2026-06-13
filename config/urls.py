from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from tours import views
from tours.forms import EmailLoginForm


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(authentication_form=EmailLoginForm), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/password-change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("accounts/password-change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("accounts/register/", views.register, name="register"),
    path("", include("tours.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
