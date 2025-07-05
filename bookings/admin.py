# bookings/admin.py
from django.contrib import admin
from .models import Availability, AvailabilityBlock, Booking

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'unavailable', 'is_booked')
    list_filter = ('date', 'unavailable', 'is_booked')

@admin.register(AvailabilityBlock)
class AvailabilityBlockAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'availability', 'treatment', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'treatment')
