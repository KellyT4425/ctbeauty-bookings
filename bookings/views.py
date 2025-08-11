from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking, Availability
from .forms import BookingForm

@login_required
def make_booking(request):
    """
    Display and process the booking creation form.

    - If the request is GET: render an empty BookingForm.
    - If the request is POST and the form is valid:
        • Associate the new Booking with the logged-in user.
        • Mark the selected Availability slot as booked.
        • Save both the slot and Booking.
        • Redirect to the bookings list page.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Rendered booking form on GET or invalid POST;
                      a redirect to 'bookings:list' on successful booking.
    """
    form = BookingForm(request.POST or None)
    if form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        # mark the slot taken
        slot = booking.availability
        slot.is_booked = True
        slot.save()
        booking.save()
        return redirect('bookings:list')
    return render(request, 'bookings/booking_form.html', {'form': form})

@login_required
def my_bookings(request):
    """
    List all bookings made by the current user.

    Fetches Booking objects belonging to request.user, including
    related Availability and Treatment to avoid extra queries,
    then renders them in the booking list template.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Rendered booking list page for the user.
    """
    bookings = Booking.objects.filter(user=request.user).select_related('availability', 'treatment')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, pk):
    """
    Display the details for a single booking.

    Retrieves a Booking by primary key that belongs to the current user,
    or raises a 404 if not found, then renders the booking detail template.

    Args:
        request (HttpRequest): The incoming HTTP request.
        pk (int): Primary key of the Booking to display.

    Returns:
        HttpResponse: Rendered booking detail page.
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def cancel_booking(request, pk):
    """
    Confirm and process cancellation of an existing booking.

    - On GET: render a confirmation page.
    - On POST: mark the associated Availability slot as free,
      delete the Booking, then redirect to the bookings list.

    Args:
        request (HttpRequest): The incoming HTTP request.
        pk (int): Primary key of the Booking to cancel.

    Returns:
        HttpResponse: Rendered confirmation page on GET or invalid POST;
                      redirect to 'bookings:list' after cancellation.
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        # free up the slot
        slot = booking.availability
        slot.is_booked = False
        slot.save()
        booking.delete()
        return redirect('bookings:list')
    return render(request, 'bookings/booking_confirm_cancel.html', {'booking': booking})

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