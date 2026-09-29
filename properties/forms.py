from django import forms

from .models import Property


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property

        fields = [
            "title",
            "slug",
            "city",
            "locality",
            "address",
            "description",
            "property_type",
            "gender",
            "monthly_rent",
            "security_deposit",
            "amenities",
            "latitude",
            "longitude",
            "cover_image",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter PG name"
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "placeholder": "luxury-girls-pg-near-coep"
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "placeholder": "Pune"
                }
            ),

            "locality": forms.TextInput(
                attrs={
                    "placeholder": "Shivajinagar"
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "placeholder": "Complete PG address"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Describe your PG..."
                }
            ),

            "monthly_rent": forms.NumberInput(
                attrs={
                    "placeholder": "8500"
                }
            ),

            "security_deposit": forms.NumberInput(
                attrs={
                    "placeholder": "5000"
                }
            ),

            "amenities": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": '["WiFi", "Food", "AC", "Laundry", "Security"]'
                }
            ),

            "latitude": forms.NumberInput(
                attrs={
                    "step": "any",
                    "placeholder": "18.5204"
                }
            ),

            "longitude": forms.NumberInput(
                attrs={
                    "step": "any",
                    "placeholder": "73.8567"
                }
            ),

            "cover_image": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*"
                }
            ),
        }