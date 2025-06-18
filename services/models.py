from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORIES = [
    ("Nails", "Nails"),
    ("Waxing/Threading", "Waxing/Threading"),
    ("Lashes", "Lashes"),

]


class Category(models.Model):
    name = models.CharField(choices=CATEGORIES, max_length=100, unique=True)

    def __str__(self):
        return self.name


class Treatment(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="treatment")
    name = models.CharField()
    description = models.TextField(max_length=200, blank=True)
    duration = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - €{self.price} | duration: {self.duration}"
