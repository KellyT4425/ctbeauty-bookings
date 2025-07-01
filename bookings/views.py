from django.shortcuts import render, get_object_or_404


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def make_booking(request):
    """TODO: display & process booking form"""
    return HttpResponse("⚙️ Booking form coming soon…")

@login_required
def my_bookings(request):
    """TODO: list this user’s bookings"""
    return HttpResponse("⚙️ Your bookings coming soon…")

@login_required
def cancel_booking(request, pk):
    """TODO: cancel or update a booking"""
    return HttpResponse(f"⚙️ Cancel booking #{pk} coming soon…")

def home(request):
    return render(request, 'base.html')
"""
B. Bookings app views
1. make_booking
URL: /bookings/make/

Access: only for logged-in users (@login_required).

Purpose: let the user pick an open time slot and create a booking.

Steps:

On GET:

Query Availability for all slots where unavailable=False, is_booked=False, and date ≥ today.

Instantiate your BookingForm, replacing its “availability” queryset with that list.

Render the form template with { "form": form }.

On POST:

Bind BookingForm(request.POST).

If valid:

Call form.save(commit=False), attach form.instance.user = request.user, then form.save().

Mark form.instance.availability.is_booked = True and save that slot.

Redirect to a confirmation page or to My Bookings.

If invalid: re-render the form with errors.

2. my_bookings
URL: /bookings/my/

Access: logged-in only.

Purpose: list all bookings made by the current user.

Steps:

Query Booking.objects.filter(user=request.user).order_by('-created_at').

Pass them into template as { "bookings": bookings }.

Template loops over each and displays the slot’s date/time, service name, status, and maybe a “Cancel” link.

3. cancel_booking
URL: /bookings/cancel/<pk>/

Access: logged-in only.

Purpose: allow a user to cancel one of their bookings.

Steps:

Lookup the Booking by pk and ensure booking.user == request.user (403 otherwise).

Set booking.status = 'CANCELLED' (or delete it) and save.

Also mark booking.availability.is_booked = False so the slot re-opens.

Redirect back to My Bookings with a success message.

C. Templates you’ll need
services/treatment_list.html

services/treatment_detail.html

bookings/make.html (form)

bookings/my.html (list)

Optionally a bookings/confirm.html for a success page

All should extend your base.html and live under templates/services/ or templates/bookings/.

D. Forms


"""