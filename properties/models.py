from django.contrib.auth.models import User
from django.db import models


# ============================================================
# PROPERTY / PG
# ============================================================

class Property(models.Model):

    PROPERTY_TYPES = [
        ("single", "Single Room"),
        ("twin", "Twin Sharing"),
        ("triple", "Triple Sharing"),
        ("studio", "Studio"),
    ]

    GENDER_CHOICES = [
        ("any", "Anyone"),
        ("male", "Male"),
        ("female", "Female"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="properties"
    )

    title = models.CharField(
        max_length=150
    )

    slug = models.SlugField(
        max_length=180,
        unique=True
    )

    city = models.CharField(
        max_length=80,
        db_index=True
    )

    locality = models.CharField(
        max_length=120
    )

    address = models.CharField(
        max_length=250
    )

    description = models.TextField()

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES
    )

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default="any"
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

    amenities = models.JSONField(
        default=list,
        blank=True
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    cover_image = models.ImageField(
        upload_to="properties/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    is_approved = models.BooleanField(
        default=False
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
                fields=["city", "monthly_rent"]
            ),

            models.Index(
                fields=["property_type", "gender"]
            ),

            models.Index(
                fields=["is_approved", "is_active"]
            ),
        ]

    def __str__(self):
        return self.title

    # ========================================================
    # RATING
    # ========================================================

    @property
    def rating(self):
        """
        Temporary rating.
        Later this will be connected
        with the Reviews system.
        """
        return 0

    # ========================================================
    # ROOM STATISTICS
    # ========================================================

    @property
    def total_rooms(self):
        return self.rooms.filter(
            is_active=True
        ).count()

    @property
    def total_beds(self):
        return Bed.objects.filter(
            room__pg=self,
            room__is_active=True
        ).count()

    @property
    def available_beds(self):
        return Bed.objects.filter(
            room__pg=self,
            room__is_active=True,
            status="vacant"
        ).count()

    @property
    def reserved_beds(self):
        return Bed.objects.filter(
            room__pg=self,
            room__is_active=True,
            status="reserved"
        ).count()

    @property
    def occupied_beds(self):
        return Bed.objects.filter(
            room__pg=self,
            room__is_active=True,
            status="occupied"
        ).count()

    @property
    def maintenance_beds(self):
        return Bed.objects.filter(
            room__pg=self,
            room__is_active=True,
            status="maintenance"
        ).count()


# ============================================================
# ROOM
# ============================================================

class Room(models.Model):

    ROOM_TYPES = [
        ("single", "Single"),
        ("double", "Double Sharing"),
        ("triple", "Triple Sharing"),
        ("four", "Four Sharing"),
    ]

    pg = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    room_number = models.CharField(
        max_length=20
    )

    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPES
    )

    floor = models.PositiveIntegerField(
        default=1
    )

    monthly_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = [
            "floor",
            "room_number"
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "pg",
                    "room_number"
                ],
                name="unique_room_per_pg"
            )
        ]

    def __str__(self):
        return (
            f"{self.pg.title} - "
            f"Room {self.room_number}"
        )

    # ========================================================
    # ROOM BED STATISTICS
    # ========================================================

    @property
    def total_beds(self):
        return self.beds.count()

    @property
    def available_beds(self):
        return self.beds.filter(
            status="vacant"
        ).count()

    @property
    def reserved_beds(self):
        return self.beds.filter(
            status="reserved"
        ).count()

    @property
    def occupied_beds(self):
        return self.beds.filter(
            status="occupied"
        ).count()

    @property
    def maintenance_beds(self):
        return self.beds.filter(
            status="maintenance"
        ).count()


# ============================================================
# BED
# ============================================================

class Bed(models.Model):

    BED_STATUS = [
        ("vacant", "Vacant"),
        ("reserved", "Reserved"),
        ("occupied", "Occupied"),
        ("maintenance", "Maintenance"),
    ]

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="beds"
    )

    bed_number = models.CharField(
        max_length=20
    )

    status = models.CharField(
        max_length=20,
        choices=BED_STATUS,
        default="vacant"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "room",
            "bed_number"
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "room",
                    "bed_number"
                ],
                name="unique_bed_per_room"
            )
        ]

    def __str__(self):
        return (
            f"Room {self.room.room_number} - "
            f"Bed {self.bed_number}"
        )

    # ========================================================
    # EASY STATUS HELPERS
    # ========================================================

    @property
    def is_vacant(self):
        return self.status == "vacant"

    @property
    def is_reserved(self):
        return self.status == "reserved"

    @property
    def is_occupied(self):
        return self.status == "occupied"

    @property
    def is_maintenance(self):
        return self.status == "maintenance"