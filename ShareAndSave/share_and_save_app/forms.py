from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    email = forms.CharField(label="email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Hasło")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        self.user = authenticate(email=email, password=password)

        if self.user is None:
            raise forms.ValidationError("Niewłaściwy login lub hasło")