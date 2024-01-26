from django.shortcuts import render

# Create your views here.

from . models import ShippingAddress, Order, OrderItem

from cart.cart import Cart


from django.http import JsonResponse

from django.db import transaction


def checkout(request):

    # Users with accounts -- Pre-fill the form

    if request.user.is_authenticated:

        try:

            # Authenticated users WITH shipping information

            shipping_address = ShippingAddress.objects.get(user=request.user.id)

            context = {'shipping': shipping_address}




            return render(request, 'payment/checkout.html', context=context)


        except:

            # Authenticated users with NO shipping information

            return render(request, 'payment/checkout.html')

    else:

        # Guest users

        return render(request, 'payment/checkout.html')



def complete_order(request):

    if request.POST.get('action') == 'post':

        office = request.POST.get('office')

        # Shopping cart information

        cart = Cart(request)


        # Get the total price of items

        total_cost = cart.get_total()


        try:
            with transaction.atomic():
                if request.user.is_authenticated:

                    order = Order.objects.create( shipping_address=office,

                    amount_paid=total_cost, user=request.user)


                    order_id = order.pk

                    for item in cart:

                        OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],

                        price=item['price'], user=request.user)

                    # Update product quantity
                    product = item['product']
                    product.quantity -= item['qty']
                    product.save()


                #  2) Create order -> Guest users without an account

                else:

                    order = Order.objects.create( shipping_address=office,

                    amount_paid=total_cost)


                    order_id = order.pk


                    for item in cart:

                        OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],

                        price=item['price'])



                order_success = True

                response = JsonResponse({'success':order_success})

                return response
        except Exception as e:
            # Handle exceptions or errors during the transaction
            print(e)
            order_success = False
            response = JsonResponse({'success': order_success})
            return response











def payment_success(request):


    # Clear shopping cart


    for key in list(request.session.keys()):

        if key == 'session_key':

            del request.session[key]



    return render(request, 'payment/payment-success.html')







def payment_failed(request):

    return render(request, 'payment/payment-failed.html')









