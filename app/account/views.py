from django.shortcuts import redirect, render

from .forms import CreateUserForm, LoginForm, UpdateUserForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from payment.models import Order, OrderItem

from store.models import Product

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate


from django.contrib.auth.decorators import login_required


from django.contrib import messages


def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()

            user.is_active = False

            user.save()

            # Email verification setup (template)

            current_site = get_current_site(request)

            subject = "Account verification email"

            message = render_to_string(
                "account/registration/email-verification.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": user_tokenizer_generate.make_token(user),
                },
            )

            user.email_user(subject=subject, message=message)

            return redirect("email-verification-sent")

    context = {"form": form}

    return render(request, "account/registration/register.html", context=context)


def email_verification(request, uidb64, token):
    # uniqueid

    unique_id = force_str(urlsafe_base64_decode(uidb64))

    user = User.objects.get(pk=unique_id)

    # Success

    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True

        user.save()

        return redirect("email-verification-success")

    # Failed

    else:
        return redirect("email-verification-failed")


def email_verification_sent(request):
    return render(request, "account/registration/email-verification-sent.html")


def email_verification_success(request):
    return render(request, "account/registration/email-verification-success.html")


def email_verification_failed(request):
    return render(request, "account/registration/email-verification-failed.html")


def my_login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect("dashboard")

    context = {"form": form}

    return render(request, "account/my-login.html", context=context)


# logout


def user_logout(request):
    try:
        for key in list(request.session.keys()):
            if key == "session_key":
                continue

            else:
                del request.session[key]

    except KeyError:
        pass

    messages.success(request, "Logout success")

    return redirect("store")


@login_required(login_url="my-login")
def dashboard(request):
    return render(request, "account/dashboard.html")


@login_required(login_url="my-login")
def profile_management(request):
    # Updating our user's username and email

    user_form = UpdateUserForm(instance=request.user)

    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            messages.info(request, "Update success!")

            return redirect("dashboard")

    context = {"user_form": user_form}

    return render(request, "account/profile-management.html", context=context)


@login_required(login_url="my-login")
def delete_account(request):
    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        user.delete()

        messages.error(request, "Account deleted")

        return redirect("store")

    return render(request, "account/delete-account.html")


@login_required(login_url="my-login")
def track_orders(request):
    try:
        orders = OrderItem.objects.filter(user=request.user)
        print(orders)
        context = {"orders": orders}

        return render(request, "account/track-orders.html", context=context)

    except:
        return render(request, "account/track-orders.html")


@login_required(login_url="my-login")
def track_listings(request):
    try:
        listings = Product.objects.filter(seller=request.user.email)
        context = {"listings": listings}

        return render(request, "account/track-listings.html", context=context)

    except:
        return render(request, "account/track-listings.html")


def delete_listing(request, listing_id):
    listing = get_object_or_404(Product, id=listing_id)
    print(listing)
    if request.method == "POST":
        listing.delete()
        return redirect("store")  # Redirect to the page displaying user's listings

    return render(request, "delete_listing_confirm.html", {"listing": listing})
