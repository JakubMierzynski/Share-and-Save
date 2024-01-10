from django.shortcuts import render
from django.views import View

class LandingPage(View):
    def get(self, request):

        return render(request, "share_and_save_app/index.html")


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
