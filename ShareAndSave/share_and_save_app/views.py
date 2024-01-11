from django.contrib.auth import login, authenticate
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from share_and_save_app.forms import LoginForm
from django.views.decorators.csrf import csrf_exempt

from share_and_save_app.models import Donation


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
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect("main")
        else:
            return HttpResponse("Brak użytkownika")




class RegisterView(View):
    def get(self, request):
        return render(request, "share_and_save_app/register.html")
