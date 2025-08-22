from django import forms
from django.utils import timezone
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

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
        queryset=Category.objects.all(), required=False, empty_label="Select Category"
    )
    class Meta:
        model = Booking
        fields = ["category", "treatment", "availability", "notes"]
        widgets = {
            "treatment": forms.Select(attrs={"class": "form-select"}),
            "availability": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
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
        self.edit_only_availability = kwargs.pop("edit_only_availability", False)
        selected_category = kwargs.pop("category_id", None)
        super().__init__(*args, **kwargs)


        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.layout = Layout("treatment", "availability", "notes")
        self.helper.add_input(Submit("submit", "Book Now", css_class="btn-primary"))

        self.fields["availability"].required = True
        self.fields["availability"].empty_label = "Select a time"


        if selected_category:
            self.fields["treatment"].queryset = Treatment.objects.filter(
                category=selected_category
            )
            self.fields["category"].initial = selected_category
        elif self.instance and getattr(self.instance, "treatment_id", None):
            # editing: ensure current treatment is available in the list
            cat_id = self.instance.treatment.category_id
            self.fields["treatment"].queryset = Treatment.objects.filter(category_id=cat_id)
            self.fields["category"].initial = cat_id
        else:
            self.fields["treatment"].queryset = Treatment.objects.none()


        now_local = timezone.localtime()
        today = now_local.date()
        current_time = now_local.time()
        availability_qs = (
            Availability.objects.filter(unavailable=False, is_booked=False)
            .filter(Q(date__gt=today) | Q(date=today, start_time__gte=current_time))
            .order_by("date", "start_time")
        )

        selected_treatment_id = self.data.get("treatment") or self.initial.get("treatment") \
                                or getattr(self.instance, "treatment_id", None)
        if selected_treatment_id:
            try:
                treatment_obj = Treatment.objects.get(pk=selected_treatment_id)
                if hasattr(treatment_obj, "duration"):
                    if treatment_obj.duration == 30:
                        availability_qs = availability_qs.filter(duration=30)
                    else:
                        availability_qs = availability_qs.filter(duration__in=[30, 60])
            except Treatment.DoesNotExist:
                pass

        self.fields["availability"].queryset = availability_qs


        def _label(slot):
            return f"{slot.date:%a %d %b} {slot.start_time.strftime('%H:%M')} – {slot.end_time.strftime('%H:%M')}"
        self.fields["availability"].label_from_instance = _label


        if self.edit_only_availability and self.instance and self.instance.pk:
            for name in ("category", "treatment", "notes"):
                if name in self.fields:
                    self.fields[name].disabled = True
                    self.fields[name].required = False
                    self.fields[name].help_text = "Not editable on an existing booking."


    def clean(self):
        """
        Server-side guard for edit-only mode:
        prevent changes to Category/Treatment/Notes when editing.
        """
        cleaned = super().clean()
        if self.edit_only_availability and self.instance and self.instance.pk:
            for name in ("category", "treatment", "notes"):
                if name in self.changed_data:
                    self.add_error(name, "To change this, cancel the booking and make a new one.")
        return cleaned
