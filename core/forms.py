from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label="First name", max_length=150, required=True)
    last_name  = forms.CharField(label="Last name",  max_length=150, required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name  = self.cleaned_data["last_name"].strip()
        user.save()
        return user
