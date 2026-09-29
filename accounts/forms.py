from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True
    )

    ROLE_CHOICES = [
        ("tenant", "I want a PG"),
        ("owner", "I have a PG"),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]
        