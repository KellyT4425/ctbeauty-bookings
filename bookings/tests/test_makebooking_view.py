from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from services.models import Category, Treatment
from ..models import Availability, Booking

# Create your tests here.

User = get_user_model()


class TestMakeBookingView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="tester", email="user@test.com", password="pw12345")

        self.cat = Category.objects.create(name="Nails")
        self.treatment = Treatment.objects.create(
            name="Gel Polish - Fingers",
            category=self.cat,
            duration=30,
            price=25
        )

        # Availability
        start_date = timezone.now() + timedelta(days=1, hours=1)

        self.slot = Availability.objects.create(
            date=start_date.date(),
            start_time=start_date.time().replace(second=0, microsecond=0),
            end_time=(start_date + timedelta(minutes=30)
                      ).time().replace(second=0, microsecond=0),
            duration=30,
            is_booked=False,
        )

        self.url_create = reverse("bookings:create")
        self.url_list = reverse("bookings:list")

    def test_get_booking_requires_login(self):
        """GET should return the booking form template"""
        resp = self.client.get(self.url_create, {"category": self.cat.id})
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login", resp.url)

    def test_get_booking_form_authenticated(self):
        self.client.login(username="tester", password="pw12345")
        resp = self.client.get(self.url_create, {"category": self.cat.id})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "bookings/booking_form.html")
        self.assertIn("form", resp.context)

    def test_post_valid_booking_creates_booking(self):
        """POST valid data should create booking and mark slot booked"""
        self.client.login(email="user@test.com", password="pw12345")
        resp = self.client.post(
            self.url_create,
            {
                "category": self.cat.id,
                "treatment": self.treatment.id,
                "availability": self.slot.id,
                "notes": "test note",
            },
        )
        self.assertEqual(resp.status_code, 302)  # redirect
        self.assertTrue(Booking.objects.filter(
            user=self.user, availability=self.slot).exists())

        self.slot.refresh_from_db()
        self.assertTrue(self.slot.is_booked)
