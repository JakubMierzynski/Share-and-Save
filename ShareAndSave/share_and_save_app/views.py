from django.contrib.auth import login, authenticate
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from share_and_save_app.models import Donation, User


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


class AddDonationView(View):
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
            # Redirect to a success page.
            return redirect("main")

        elif auth is None:
            messages.add_message(request, messages.SUCCESS, 'Niepoprawne hasło')
            return redirect("login")




class RegisterView(View):
    def get(self, request):
        return render(request, "share_and_save_app/register.html")
