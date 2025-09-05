from datetime import datetime, timedelta
from .models import Availability


def create_slots_for_date(date, start_time, end_time, slot_minutes=30):
    """
    Generate Availability slots on a given date by slicing the time range into
    equal chunks defined by slot_minutes. Skips slots that already exist.

    Each created Availability will have:
      - date
      - start_time
      - end_time
      - duration (in minutes)
      - is_booked=False
    """
    current = datetime.combine(date, start_time)
    end_dt = datetime.combine(date, end_time)
    slots_to_create = []

    # gather all existing (start,end) pairs for that date
    existing = {
        (a.start_time, a.end_time)
        for a in Availability.objects.filter(date=date)
    }

    while current + timedelta(minutes=slot_minutes) <= end_dt:
        st = current.time()
        et = (current + timedelta(minutes=slot_minutes)).time()

        if (st, et) not in existing:
            slots_to_create.append(
                Availability(
                    date=date,
                    start_time=st,
                    end_time=et,
                    duration=slot_minutes,
                    is_booked=False,
                )
            )

        current += timedelta(minutes=slot_minutes)

    return Availability.objects.bulk_create(slots_to_create)
