from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORIES = [
    ("Nails", "Nails"),
    ("Waxing/Threading", "Waxing/Threading"),
    ("Lashes", "Lashes"),
    ("MakeUp", "Makeup"),

]


class Category(models.Model):
    name = models.CharField(choices=CATEGORIES, max_length=100, unique=True, help_text = "Please select a Category.")
    slug = models.SlugField(max_length=60, unique=True, null=True, blank=True, help_text="Helpful URL Identifier.")

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return dict(CATEGORIES)[self.name]


class Treatment(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="treatments")
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    duration = models.IntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} - €{self.price} | duration: {self.duration}"
