from django.shortcuts import render, redirect

from .models import Category, Product

from django.shortcuts import get_object_or_404

from .forms import ProductForm

from django.contrib.auth.decorators import login_required

from PIL import Image


def store(request):
    # all_products = Product.objects.all()
    all_products = Product.objects.filter(quantity__gt=0)

    context = {"my_products": all_products}

    return render(request, "store/store.html", context)


def categories(request):
    all_categories = Category.objects.all()

    return {"all_categories": all_categories}


def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    return render(
        request,
        "store/list-category.html",
        {"category": category, "products": products},
    )


def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    context = {"product": product}

    return render(request, "store/product-info.html", context)


@login_required
def upload_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
<<<<<<< Updated upstream
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.email

            form.save()

            return redirect('store')
=======
        print("PRINTING HERE")
        print(form)
        print("End of PRINTING HERE")

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.email

            form.save()

            return redirect("store")
>>>>>>> Stashed changes
    else:
        form = ProductForm()
    return render(request, "store/upload_product.html", {"form": form})


@login_required
def edit_product(request, listing_id):
    listing = get_object_or_404(Product, id=listing_id)

    # Check if the current user is the seller of the product
    if listing.seller.email != request.user.email:
        print("NOT OG USER")  # It's better to use logging instead of print
        return redirect(
            "name_of_your_store_view"
        )  # Replace with your store's view name
    else:
        context = {"my_products": listing}
        return render(request, "store/edit_product.html", context)
