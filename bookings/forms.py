from django import forms

from properties.models import Bed

from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            "bed",
            "move_in_date",
            "duration_months",
            "tenant_message",
        ]

        widgets = {
            "bed": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "move_in_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "duration_months": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 24,
                }
            ),

            "tenant_message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write a message to the PG owner...",
                }
            ),
        }

    def __init__(self, *args, property_obj=None, **kwargs):

        super().__init__(*args, **kwargs)

        # No property supplied
        if property_obj is None:
            self.fields["bed"].queryset = Bed.objects.none()
            return

        # Only active rooms + vacant beds of this PG
        self.fields["bed"].queryset = Bed.objects.filter(
            room__pg=property_obj,
            room__is_active=True,
            status="vacant",
        ).select_related("room")

        # Better bed names in dropdown
        self.fields["bed"].label_from_instance = (
            lambda bed:
            f"Room {bed.room.room_number} - Bed {bed.bed_number}"
        )

        self.fields["move_in_date"].required = True
        self.fields["duration_months"].required = True
        self.fields["tenant_message"].required = False