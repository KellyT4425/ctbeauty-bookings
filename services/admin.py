from django.contrib import admin
from .models import Category, Treatment

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration')
    list_filter = ('category',)
    search_fields = ('name', 'description')
