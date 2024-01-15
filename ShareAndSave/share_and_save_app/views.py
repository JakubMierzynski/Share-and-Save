import re

from django.contrib.auth import login, authenticate, logout
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from share_and_save_app.models import Donation, User
from django.core.validators import validate_email
from django.contrib.auth.mixins import LoginRequiredMixin


class LandingPageView(View):
    def get(self, request):
        donations = Donation.objects.all()
        donations_quantity = donations.aggregate(Sum('quantity')).get('quantity__sum')

        supported_institutions = set()
        for donation in donations:
            supported_institutions.add(donation.institution_id)

        ctx = {'donations_quantity': donations_quantity,
               'supported_institutions_counter': len(supported_institutions),
               }

        return render(request, "share_and_save_app/index.html", context=ctx)



class AddDonationView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        return render(request, "share_and_save_app/form.html")


class DonationConfirmationView(View):
    def get(self, request):
        return render(request, "share_and_save_app/form-confirmation.html")


# class LoginView(View):
#     def get(self, request):
#         return render(request, "share_and_save_app/login.html")


@csrf_exempt
def LoginView(request):
    if request.method == "GET":
        return render(request, "share_and_save_app/login.html")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

        except ObjectDoesNotExist:
            messages.add_message(request, messages.SUCCESS, f'Nie istnieje konto powiązane z adresem {email}. Utwórz je tutaj')
            return redirect("register")


        auth = authenticate(request, email=email, password=password)

        if auth is not None:
            login(request, user)
            print(user.is_authenticated)

            redirect_to = request.GET.get('next', None)
            if redirect_to:
                return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponseRedirect(reverse_lazy("main"))

        elif auth is None:
            messages.add_message(request, messages.SUCCESS, 'Niepoprawne hasło')
            return redirect("login")


@csrf_exempt
def RegisterView(request):
    if request.method == "GET":
        return render(request, "share_and_save_app/register.html")

    if request.method == "POST":
        name = request.POST.get("name")
        lastname = request.POST.get("surname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        # Validation
        if len(name) < 1:
            messages.add_message(request, messages.SUCCESS, f'Nie podano imienia. Ponownie wypełnij formularz')
            return redirect("register")

        if len(lastname) < 1:
            messages.add_message(request, messages.SUCCESS, f'Nie podano nazwiska. Ponownie wypełnij formularz')
            return redirect("register")

        if password != password2:
            messages.add_message(request, messages.SUCCESS, f'Hasła nie są identyczne. Ponownie wypełnij formularz')
            return redirect("register")

        try:
            validate_email(email)
        except ValidationError as e:
            messages.add_message(request, messages.SUCCESS, f'Podany adres mailowy jest niepoprawny. Ponownie wypełnij formularz')
            return redirect("register")


        # Create User
        user = User.objects.create_user(email=email,
                                        password=password,
                                        first_name=name,
                                        last_name=lastname)

        # Redirect to login
        messages.add_message(request, messages.SUCCESS, f'Pomyślnie utworzono konto. Zaloguj się')
        return redirect("login")


def LogoutView(request):
    logout(request)
    return redirect('main')
