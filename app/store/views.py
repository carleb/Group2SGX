from django.shortcuts import render, redirect

from . models import Category, Product

from django.shortcuts import get_object_or_404

from .forms import ProductForm

from django.contrib.auth.decorators import login_required

from PIL import Image

from payment.models import OrderItem

from django.db.models import Sum, F, ExpressionWrapper, fields


def store(request):

    # all_products = Product.objects.all()
    all_products = Product.objects.filter(quantity__gt=0)

    context = {'my_products':all_products}

    return render(request, 'store/store.html', context)



def categories(request):

    all_categories = Category.objects.all()

    return {'all_categories': all_categories}



def list_category(request, category_slug=None):

    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)


    return render(request, 'store/list-category.html', {'category':category, 'products':products})



def product_info(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug)

    context = {'product': product}

    return render(request, 'store/product-info.html', context)


@login_required
def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        # if form.is_valid():
        product = form.save(commit=False)
        product.seller = request.user.email

        form.save()

        return redirect('store')
    else:
        form = ProductForm()
    return render(request, 'store/upload_product.html', {'form': form})



def get_top_items(request):

    context = {}

    top_order_item_by_qty = OrderItem.objects.values('product').annotate(
        total_quantity_sold=Sum('quantity')
    ).order_by('-total_quantity_sold').first()

    if top_order_item_by_qty:

        product_name = OrderItem.objects.filter(product=top_order_item_by_qty['product'])[0].product

        total_quantity_sold = top_order_item_by_qty['total_quantity_sold']

        context.update({'product_name_for_qty': product_name, 
                   'total_quantity_sold': total_quantity_sold})  
     

    top_order_item_by_amt_raise = OrderItem.objects.values('product').annotate(
        total_amount_sold=Sum(F('price') * F('quantity'))
    ).order_by('-total_amount_sold').first()

    if top_order_item_by_amt_raise:
        product_name = OrderItem.objects.filter(product=top_order_item_by_amt_raise['product'])[0].product

        total_amount_sold = top_order_item_by_amt_raise['total_amount_sold']

        context.update({'product_name_for_price': product_name, 
                   'total_amount_sold': total_amount_sold})
    
    if len(context):
        return render(request, 'store/sales-report.html', context)

    else:
        return render(request, 'store/sales-report.html')

