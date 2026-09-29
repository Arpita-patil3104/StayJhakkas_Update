from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from properties.models import Property

from .models import Wishlist


@login_required
def toggle_wishlist(request, property_id):

    property_obj = get_object_or_404(
        Property,
        id=property_id,
        is_active=True,
        is_approved=True
    )

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        property=property_obj
    )

    if not created:
        wishlist_item.delete()

    return redirect(
        "property_detail",
        slug=property_obj.slug
    )


@login_required
def wishlist_list(request):

    wishlists = Wishlist.objects.filter(
        user=request.user
    ).select_related("property")

    return render(
        request,
        "wishlist/wishlist.html",
        {"wishlists": wishlists}
    )