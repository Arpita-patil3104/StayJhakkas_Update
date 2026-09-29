from django.urls import path
from . import views


urlpatterns = [

    path(
        "create/<int:property_id>/",
        views.create_booking,
        name="create_booking"
    ),

    path(
        "my/",
        views.my_bookings,
        name="my_bookings"
    ),

    path(
        "owner/",
        views.owner_bookings,
        name="owner_bookings"
    ),

    path(
        "owner/<int:booking_id>/approve/",
        views.approve_booking,
        name="approve_booking"
    ),

    path(
        "owner/<int:booking_id>/reject/",
        views.reject_booking,
        name="reject_booking"
    ),

    path(
        "<int:booking_id>/",
        views.booking_detail,
        name="booking_detail"
    ),
]