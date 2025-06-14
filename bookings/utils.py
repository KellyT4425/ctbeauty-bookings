from datetime import datetime, timedelta
from .models import Availability


def create_slots_for_date(date, start_time, end_time):
    current = datetime.combine(date, start_time)
    end = datetime.combine(date, end_time)
    slots = []

    while current + timedelta(minutes=15) <= end:
        slot = Availability(
            date=date,
            start_time=current.time(),
            end_time=(current + timedelta(minutes=15)).time(),
            is_booked=False,
        )
        slots.append(slot)
        current += timedelta(minutes=15)

    Availability.objects.bulk_create(slots)
