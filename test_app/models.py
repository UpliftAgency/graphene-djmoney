from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField


class User(AbstractUser):
    pass


class Product(models.Model):
    creator = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    cost = MoneyField(
        max_digits=settings.CURRENCY_MAX_DIGITS,
        decimal_places=settings.CURRENCY_DECIMAL_PLACES,
        default_currency=settings.BASE_CURRENCY,
        null=True,
        blank=True,
    )
