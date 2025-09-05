from django import forms
from allauth.account.forms import SignupForm
from django.core.validators import RegexValidator

name_validator = RegexValidator(
    r'^[A-Za-z\s]+$', "Only letters and spaces are allowed.")

username_validator = RegexValidator(
    regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$',
    message="Username can only contain both letters and numbers.",
    code="invalid_username"
)


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[name_validator],
        widget=forms.TextInput(attrs={
            "pattern": r"[A-Za-z ]+",
            "title": "Only letters and spaces are allowed."})
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[name_validator],
        widget=forms.TextInput(attrs={
            "pattern": r"[A-Za-z ]+",
            "title": "Only letters and spaces are allowed."
        })
    )

    username = forms.CharField(
        max_length=10,
        required=True,
        validators=[username_validator],
        widget=forms.TextInput(attrs={
            "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$",
            "title": "Only letters and numbers are allowed."
        })
    )
