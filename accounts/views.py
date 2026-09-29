from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from bookings.models import Booking
from properties.models import Property


# =========================
# REGISTER
# =========================

def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not email or not password:
            messages.error(
                request,
                "Please fill all required fields."
            )
            return redirect("register")

        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "Username already exists."
            )
            return redirect("register")

        if User.objects.filter(email__iexact=email).exists():
            messages.error(
                request,
                "Email is already registered."
            )
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        messages.success(
            request,
            "Account created successfully. Welcome!"
        )

        return redirect("home")

    return render(
        request,
        "accounts/register.html"
    )


# =========================
# LOGIN
# =========================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        if not username or not password:
            messages.error(
                request,
                "Please enter username and password."
            )
            return redirect("login")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            next_url = request.GET.get("next")

            if next_url:
                return redirect(next_url)

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "accounts/login.html"
    )


# =========================
# LOGOUT
# =========================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("home")


# =========================
# DASHBOARD
# =========================

@login_required
def dashboard(request):

    properties = Property.objects.filter(
        owner=request.user
    )

    bookings = Booking.objects.filter(
        property__owner=request.user
    )

    context = {
        "properties": properties,

        "total_properties": properties.count(),

        "total_rooms": sum(
            p.total_rooms
            for p in properties
        ),

        "total_beds": sum(
            p.total_beds
            for p in properties
        ),

        "available_beds": sum(
            p.available_beds
            for p in properties
        ),

        "pending_bookings": bookings.filter(
            status="pending"
        ).count(),

        "approved_bookings": bookings.filter(
            status="approved"
        ).count(),

        "total_bookings": bookings.count(),
    }

    return render(
        request,
        "accounts/owner_dashboard.html",
        context
    )