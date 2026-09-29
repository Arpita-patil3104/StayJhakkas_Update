from django.contrib.auth.models import User
from django.db import models

from properties.models import Property


class Review(models.Model):

    RATING_CHOICES = [
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "property"],
                name="unique_user_property_review"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.property.title} - {self.rating}/5"