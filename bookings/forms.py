from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Booking, Availability

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['availability', 'treatment', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crispy helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        # add a submit button
        self.helper.add_input(Submit('submit', 'Book Now', css_class='btn-primary'))

        # Only show slots that are not marked unavailable or already booked
        self.fields['availability'].queryset = (
            Availability.objects
            .filter(unavailable=False, is_booked=False)
            .order_by('date', 'start_time')
        )
        self.fields['availability'].label_from_instance = lambda slot: (
            f"{slot.date} {slot.start_time:%H:%M}–{slot.end_time:%H:%M}"
        )