# bookings/utils.py
from datetime import datetime, timedelta
from .models import Availability

def create_slots_for_date(date, start_time, end_time, slot_minutes=30):
    current = datetime.combine(date, start_time)
    end     = datetime.combine(date, end_time)
    slots   = []

    # gather all existing (start,end) pairs for this date
    existing = {
        (a.start_time, a.end_time)
        for a in Availability.objects.filter(date=date)
    }

    while current + timedelta(minutes=slot_minutes) <= end:
        st = current.time()
        et = (current + timedelta(minutes=slot_minutes)).time()
        if (st, et) not in existing:
            slots.append(Availability(
                date=date,
                start_time=st,
                end_time=et,
                is_booked=False,
            ))
        current += timedelta(minutes=slot_minutes)

    return Availability.objects.bulk_create(slots)
