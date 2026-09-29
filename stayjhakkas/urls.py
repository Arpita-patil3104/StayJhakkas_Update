from django.contrib import admin
from django.urls import include, path


urlpatterns = [

    # Admin
    path(
        "admin/",
        admin.site.urls
    ),

    # Home
    path(
        "",
        include("core.urls")
    ),

    # Properties / PG
    path(
        "properties/",
        include("properties.urls")
    ),

    # Login / Register / Dashboard
    path(
        "accounts/",
        include("accounts.urls")
    ),

    # Bookings
    path(
        "bookings/",
        include("bookings.urls")
    ),

    # Wishlist
    path(
        "wishlist/",
        include("wishlist.urls")
    ),

    # Reviews
    path(
        "reviews/",
        include("reviews.urls")
    ),
]