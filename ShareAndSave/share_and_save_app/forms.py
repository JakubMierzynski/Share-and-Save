from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm


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



class PasswordChangeForm(DjangoPasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(), label="Stare hasło")
    new_password1 = forms.CharField(widget=forms.PasswordInput(), label="Nowe hasło")
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label="Potwierdź hasło")

    class Meta:
        fields = ("old_password", "new_password1", "new_password2")

    # def clean(self):
    #     cleaned_data = super().clean()
    #     old_password = cleaned_data.get("old_password")
    #     new_password = cleaned_data.get("new_password")
    #     new_password_confirm = cleaned_data.get("new_password_confirm")