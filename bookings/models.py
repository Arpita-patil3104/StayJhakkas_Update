from django.contrib.auth.models import User
from django.db import models

from properties.models import Property, Room, Bed


class Booking(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings"
    )

    bed = models.ForeignKey(
        Bed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings"
    )

    move_in_date = models.DateField()

    duration_months = models.PositiveIntegerField(
        default=1
    )

    monthly_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    security_deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        db_index=True
    )

    tenant_message = models.TextField(
        blank=True
    )

    owner_message = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["tenant", "status"]
            ),
            models.Index(
                fields=["property", "status"]
            ),
        ]

    def __str__(self):
        return (
            f"{self.tenant.username} - "
            f"{self.property.title}"
        )

    def get_total_amount(self):
        return (
            self.monthly_rent * self.duration_months
            + self.security_deposit
        )