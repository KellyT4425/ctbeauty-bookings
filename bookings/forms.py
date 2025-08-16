from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from .models import Booking, Availability
from services.models import Category, Treatment

class BookingForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False, empty_label="Select Category"
    )

    class Meta:
        model = Booking
        fields = ["category", "treatment", "availability", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        selected_category = kwargs.pop("category_id", None)
        super().__init__(*args, **kwargs)

        # Crispy helper
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.layout = Layout("treatment", "availability", "notes")
        self.helper.add_input(Submit("submit", "Book Now", css_class="btn-primary"))

        # always require availability
        self.fields["availability"].required = True

        self.fields['availability'].widget.attrs['size'] = 5


        # Filter treatments by category
        if selected_category:
            self.fields["treatment"].queryset = Treatment.objects.filter(category=selected_category)
        else:
            self.fields["treatment"].queryset = Treatment.objects.none()

        # Base queryset of free slots
        availability_qs = Availability.objects.filter(unavailable=False, is_booked=False)

        # Filter availability to match duration of the selected treatment
        selected_treatment_id = self.data.get("treatment")
        if selected_treatment_id:
            try:
                treatment_obj = Treatment.objects.get(pk=selected_treatment_id)
                # assumes availability.duration and treatment.duration are stored in minutes
                # e.g. allow both 30-minute and 60-minute slots
                if treatment_obj.duration == 30:
                    availability_qs = availability_qs.filter(duration=30)
                else:
                    availability_qs = availability_qs.filter(duration__in=[30, 60])
            except Treatment.DoesNotExist:
                pass



            except Treatment.DoesNotExist:
                pass

        self.fields["availability"].queryset = availability_qs
