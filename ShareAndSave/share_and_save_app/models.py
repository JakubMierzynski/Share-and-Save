from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import validate_email
from django.utils.timezone import now
import datetime


# Manager for User class
class CustomUserManager(UserManager):
    def _get_email(self,
                   email: str):
        validate_email(email)
        return self.normalize_email(email)

    def _create_user(self,
                     first_name: str,
                     last_name: str,
                     email: str,
                     password: str,
                     commit: bool,
                     is_staff: bool = False,
                     is_superuser: bool = False
                     ):

        email = self._get_email(email)

        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    username=email,
                    is_staff=is_staff,
                    is_superuser=is_superuser)
        user.set_password(password)

        if commit:
            user.save()

        return user

    def create_user(self, first_name: str, last_name: str, email: str, password: str, commit: bool = True):
        return self._create_user(first_name, last_name, email, password, commit=commit)

    def create_superuser(self, first_name: str, last_name: str, email: str, password: str, commit: bool = True):
        return self._create_user(first_name, last_name, email, password, is_staff=True, is_superuser=True, commit=commit)


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()





INSTITUTION_TYPES = (
    ("Fundacja", 1),
    ("Organizacja pozarządowa", 2),
    ("Zbiórka lokalna", 3),
)


class Category(models.Model):
    name = models.CharField(max_length=150, blank=False, verbose_name="Kategoria")


class Institution(models.Model):
    name = models.CharField(max_length=150, blank=False, verbose_name="Nazwa instytucji")
    description = models.TextField(blank=False, verbose_name="Opis instytucji/organizacji/fundacji")
    type = models.CharField(max_length=150, choices=INSTITUTION_TYPES, default="Fundacja", verbose_name="Typ organizacji")
    categories = models.ManyToManyField(Category, verbose_name="Kategoria")


class Donation(models.Model):
    quantity = models.IntegerField(verbose_name="Liczba worków")
    categories = models.ManyToManyField(Category, verbose_name="Kategoria")
    institution = models.ForeignKey(Institution, verbose_name="Instytucja", on_delete=models.CASCADE)
    address = models.CharField(max_length=150, verbose_name="Ulica i numer domu/mieszkania")
    phone_number = models.CharField(max_length=9, verbose_name="Number telefonu")
    city = models.CharField(max_length=50, verbose_name="Miasto")
    zip_code = models.CharField(max_length=5, verbose_name="Kod pocztowy")
    pick_up_date = models.DateField(default=now(), verbose_name="Data odbioru")
    pick_up_time = models.TimeField(default=datetime.datetime.now().strftime("%H:%M:%S"), verbose_name="Godzina odbioru")
    pick_up_comment = models.TextField(verbose_name="Dodatkowe informacje")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)


