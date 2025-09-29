from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from ems_app.models import Employee


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name", "id": "firstName"})
    )
    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name", "id": "lastName"})
    )
    username = forms.CharField(
        max_length=150, required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username", "id": "username"})
    )
    email = forms.EmailField(
        max_length=254, required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address", "id": "email"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password", "id": "password1"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password", "id": "password2"})
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        # Save the User first
        user = super().save(commit=commit)

        # Save Employee table record too
        Employee.objects.create(
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            email=self.cleaned_data.get("email"),
            phone="",  # add phone input in form if you want
            password=self.cleaned_data.get("password1")  # ⚠️ stores plain password (NOT secure)
        )
        return user