from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PropertyForm
from .models import Property


def property_list(request):

    properties = Property.objects.filter(
        is_active=True,
        is_approved=True
    ).select_related("owner")


    city = request.GET.get(
        "city",
        ""
    ).strip()


    property_type = request.GET.get(
        "property_type",
        ""
    ).strip()


    gender = request.GET.get(
        "gender",
        ""
    ).strip()


    max_rent = request.GET.get(
        "max_rent",
        ""
    ).strip()


    if city:

        properties = properties.filter(
            city__icontains=city
        )


    if property_type:

        properties = properties.filter(
            property_type=property_type
        )


    if gender:

        properties = properties.filter(
            gender=gender
        )


    if max_rent:

        try:

            properties = properties.filter(
                monthly_rent__lte=float(max_rent)
            )

        except ValueError:

            pass


    return render(

        request,

        "properties/property_list.html",

        {
            "properties": properties,
            "city": city,
            "property_type": property_type,
            "gender": gender,
            "max_rent": max_rent,
        }

    )



def property_detail(request, slug):

    property_obj = get_object_or_404(

        Property,

        slug=slug,

        is_active=True,

        is_approved=True

    )


    return render(

        request,

        "properties/property_detail.html",

        {
            "property": property_obj
        }

    )



@login_required
def add_property(request):

    if request.method == "POST":

        form = PropertyForm(
            request.POST,
            request.FILES
        )


        if form.is_valid():

            property_obj = form.save(
                commit=False
            )

            property_obj.owner = request.user

            property_obj.save()


            return redirect(

                "property_detail",

                slug=property_obj.slug

            )


    else:

        form = PropertyForm()


    return render(

        request,

        "properties/property_form.html",

        {
            "form": form
        }

    )