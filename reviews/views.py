from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from properties.models import Property

from .forms import ReviewForm


@login_required
def add_review(request, property_id):

    property_obj = get_object_or_404(
        Property,
        id=property_id,
        is_active=True,
        is_approved=True
    )

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.user = request.user
            review.property = property_obj

            review.save()

    return redirect(
        "property_detail",
        slug=property_obj.slug
    )