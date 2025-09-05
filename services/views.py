from django.shortcuts import render
from .models import Category

# Create your views here.


def home(request):
    """
    Simple landing/homepage view.
    """
    return render(request, 'home.html')


def services_list(request):
    """
    Display all service categories with their treatments/prices.
    """
    categories = Category.objects.prefetch_related('treatments')
    return render(request, 'services/services_list.html', {
        'categories': categories
    })
