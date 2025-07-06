from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
"""
1. treatment_list
URL: /services/

Purpose: show all available services, grouped by category.

Steps:

Fetch all Category objects (with their related Treatments).

Pass them into the template context, e.g. { "categories": categories }.

Render a template that loops over each category and under it each treatment name (with link to the detail page).

2. treatment_detail
URL: /services/<slug>/

Purpose: show full info for one service (name, description, price, duration).

Steps:

Look up the Treatment by its slug (404 if not found).

Pass it into the template as { "treatment": treatment }.

Render a detail page that shows the fields and a “Book this service” button (linking to /bookings/make/).



"""

def treatment_list(request):
    """TODO: list all treatments by category"""
    return HttpResponse("⚙️ Treatment list coming soon…")


def treatment_detail(request, slug):
    """TODO: show one treatment’s detail"""
    return HttpResponse(f"⚙️ Treatment detail for “{slug}” coming soon…")

def home(request):
    return render(request, 'home.html')