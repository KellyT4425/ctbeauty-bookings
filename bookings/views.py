from django.shortcuts import render
from .models import Availability


def available_slots(request):
    slots = Availability.objects.filter(
        is_booked=False).order_by('date', 'start_time')
    return render(request, 'available_slots.html', {'slots': slots})
