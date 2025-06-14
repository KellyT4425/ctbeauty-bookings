from django.contrib import admin
from .models import Availability, AvailabilityBlock  # , Booking
from .utils import create_slots_for_date

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
    list_display = ('date', 'start_time', 'end_time',
                    'is_booked')
    list_filter = ('date', 'is_booked')
    ordering = ('date', 'start_time')


@admin.action(description="Create 15-minute slots for selected availability blocks")
def create_slots(modeladmin, request, queryset):
    for block in queryset:
        create_slots_for_date(block.date, block.start_time,
                              block.end_time)
    modeladmin.message_user(request, "Slots created!")


@admin.register(AvailabilityBlock)
class AvailabilityBlockAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time')
    actions = [create_slots]
