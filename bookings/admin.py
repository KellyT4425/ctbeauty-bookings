from django.contrib import admin
from .models import Availability  # , Booking

# Register your models here.


# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
# list_display = ('user', 'treatment', 'date',
# 'time', 'status', 'created_at')
# list_filter = ('status', 'date', 'treatment')
# search_fields = ('user__username', 'treatment__name', 'date')
# ordering = ('-date', '-time')


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'start_time',
                    'end_time', 'unavailable', 'is_active')
    list_filter = ('day_of_week', 'unavailable', 'is_active')
