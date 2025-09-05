from django import forms
from django.utils import timezone
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
import re

from .models import Booking, Availability
from services.models import Category, Treatment


class BookingForm(forms.ModelForm):
    """
    Booking form for create/edit.

    Supports:
    - optional category prefilter (`category_id`)
    - edit-only mode (only Availability editable)
    - future/free availability filtered by treatment duration
    - crispy-forms layout and nicer slot labels
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=True,
        empty_label="Select Category", label="Category",
    )

    class Meta:
        model = Booking
        fields = ["category", "treatment", "availability", "notes"]
        widgets = {
            "treatment": forms.Select(attrs={"class": "form-select"}),
            "availability": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"rows": 4,
                                           "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form.

        - Reads `edit_only_availability` and `category_id` flags.
        - Sets crispy helper/layout.
        - Prefilters treatments by category (or instance on edit).
        - Builds availability queryset: future, unbooked slots; filters by
          selected treatment’s duration; applies readable option labels.
        - In edit-only mode, disables Category/Treatment/Notes fields.
        """
        self.edit_only_availability = kwargs.pop(
            "edit_only_availability", False)
        prefilter_category = kwargs.pop("category_id", None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.layout = Layout("category",
                                    "treatment",
                                    "availability",
                                    "notes")
        self.helper.add_input(Submit("submit", "Book Now",
                                     css_class="btn-primary"))

        self.fields["treatment"].required = True
        self.fields["treatment"].empty_label = "Select Treatment"
        self.fields["availability"].required = True
        self.fields["availability"].empty_label = "Select a date & time"

        cat_id = None
        if "category" in self.data:
            try:
                cat_id = int(self.data.get("category")) or None
            except (TypeError, ValueError):
                cat_id = None
        if not cat_id and prefilter_category:
            cat_id = prefilter_category if isinstance(
                prefilter_category, int) else getattr(prefilter_category, "pk", None)
        if not cat_id and self.initial.get("category"):
            cat_init = self.initial["category"]
            cat_id = cat_init.pk if hasattr(cat_init, "pk") else cat_init
        if not cat_id and getattr(self.instance, "treatment_id", None):
            cat_id = self.instance.treatment.category_id

        # --- Filter treatments by category (or none) ---
        if cat_id:
            self.fields["treatment"].queryset = Treatment.objects.filter(
                category_id=cat_id)
            self.fields["category"].initial = cat_id
        else:
            self.fields["treatment"].queryset = Treatment.objects.none()

        # --- Availability: future, unbooked; optionally match duration ---
        now_local = timezone.localtime()
        today, current_time = now_local.date(), now_local.time()
        availability_qs = (
            Availability.objects.filter(unavailable=False, is_booked=False)
            .filter(Q(date__gt=today) | Q(date=today, start_time__gte=current_time))
            .order_by("date", "start_time")
        )

        # If a treatment is chosen, trim slots by duration rules
        selected_treatment_id = (
            self.data.get("treatment")
            or self.initial.get("treatment")
            or getattr(self.instance, "treatment_id", None)
        )
        if selected_treatment_id:
            try:
                t = Treatment.objects.get(pk=selected_treatment_id)
                if hasattr(t, "duration"):
                    availability_qs = (
                        availability_qs.filter(duration=30)
                        if t.duration == 30 else availability_qs.filter(duration__in=[30, 60])
                    )
            except Treatment.DoesNotExist:
                pass

        self.fields["availability"].queryset = availability_qs
        self.fields["availability"].label_from_instance = lambda s: (
            f"{s.date:%a %d %b} {s.start_time:%H:%M} – {s.end_time:%H:%M}"
        )

        # --- Edit-only mode: lock non-availability fields ---
        if self.edit_only_availability and self.instance and self.instance.pk:
            for name in ("category", "treatment", "notes"):
                if name in self.fields:
                    self.fields[name].disabled = True
                    self.fields[name].required = False
                    self.fields[name].help_text = "Not editable on an existing booking."

    def clean(self):
        cleaned = super().clean()

        # Respect edit-only guard
        if self.edit_only_availability and self.instance and self.instance.pk:
            for name in ("category", "treatment", "notes"):
                if name in self.changed_data:
                    self.add_error(
                        name, "To change this, cancel the booking and make a new one.")
            return cleaned

        category = cleaned.get("category")
        treatment = cleaned.get("treatment")
        availability = cleaned.get("availability")

        # Field-level requireds are already set, but keep a friendly fallback:
        if not category:
            self.add_error("category", "Please select a category.")
        if not treatment:
            self.add_error("treatment", "Please select a treatment.")
        if not availability:
            self.add_error("availability", "Please select a time slot.")

        # Cross-field: treatment must belong to selected category
        if category and treatment and treatment.category_id != category.id:
            self.add_error(
                "treatment", "Please choose a treatment in the selected category.")

        return cleaned

    def clean_notes(self):
        """Notes optional, but reject only-spaces or numbers-only."""
        notes = self.cleaned_data.get("notes", "")
        if not notes:
            return notes
        s = notes.strip()
        if not s:
            raise forms.ValidationError("Notes cannot be only spaces.")
        if re.fullmatch(r"\d+", s):
            raise forms.ValidationError("Notes cannot be only numbers.")
        return notes
