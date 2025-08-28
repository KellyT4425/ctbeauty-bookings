from django import forms
from allauth.account.forms import SignupForm
from django.core.validators import RegexValidator


class CustomSignupForm(SignupForm):
    name_validator = RegexValidator(
        regex=r'^[A-Za-z\s]+$',
        message="Only letters and spaces are allowed."
    )

    first_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[name_validator]
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[name_validator]
    )