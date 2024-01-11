from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from share_and_save_app.models import Donation


class LandingPage(View):
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


class AddDonation(View):
    def get(self, request):
        return render(request, "share_and_save_app/form.html")


class DonationConfirmation(View):
    def get(self, request):
        return render(request, "share_and_save_app/form-confirmation.html")


class Login(View):
    def get(self, request):
        return render(request, "share_and_save_app/login.html")


class Register(View):
    def get(self, request):
        return render(request, "share_and_save_app/register.html")
