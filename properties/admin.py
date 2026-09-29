from django.contrib import admin
from .models import Property, Room, Bed


# ============================================================
# PROPERTY ADMIN
# ============================================================

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "city",
        "locality",
        "property_type",
        "monthly_rent",
        "available_beds",
        "reserved_beds",
        "occupied_beds",
        "is_approved",
        "is_active",
        "created_at",
    )

    list_filter = (
        "city",
        "property_type",
        "gender",
        "is_approved",
        "is_active",
    )

    search_fields = (
        "title",
        "city",
        "locality",
        "address",
        "description",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    list_editable = (
        "is_approved",
        "is_active",
    )


# ============================================================
# ROOM ADMIN
# ============================================================

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "room_number",
        "pg",
        "room_type",
        "floor",
        "monthly_rent",
        "total_beds",
        "available_beds",
        "reserved_beds",
        "occupied_beds",
        "maintenance_beds",
        "is_active",
    )

    list_filter = (
        "room_type",
        "floor",
        "is_active",
    )

    search_fields = (
        "room_number",
        "pg__title",
        "pg__city",
        "pg__locality",
    )


# ============================================================
# BED ADMIN
# ============================================================

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):

    list_display = (
        "bed_number",
        "room",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "bed_number",
        "room__room_number",
        "room__pg__title",
    )

    list_editable = (
        "status",
    )