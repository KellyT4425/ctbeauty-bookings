from django.shortcuts import render, get_object_or_404
from .models import Availability



def home(request):
    return render(request, 'base.html')
