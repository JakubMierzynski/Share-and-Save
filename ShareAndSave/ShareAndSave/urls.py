"""ShareAndSave URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, reverse_lazy
from share_and_save_app.views import LandingPageView,\
    AddDonationView,\
    LoginView,\
    RegisterView,\
    DonationConfirmationView, \
    LogoutView, \
    UserPageView, \
    PasswordChangeView

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name="main"),
    path('przekaz-dary/', AddDonationView.as_view(), name="make_donation"),
    path('potwierdzenie-daru/', DonationConfirmationView.as_view()),
    path('logowanie/', LoginView, name="login"),
    path('rejestracja/', RegisterView, name="register"),
    path('wyloguj/', LogoutView, name="logout"),
    path('profil/', UserPageView.as_view(), name="profile"),
    path('zmiana-danych/', PasswordChangeView.as_view(template_name="share_and_save_app/change_password.html"), name="zmiana_danych"),

]
