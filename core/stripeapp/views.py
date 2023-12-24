import os
import stripe
from django.contrib import messages
from django.urls import reverse

from dotenv import load_dotenv, find_dotenv

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView

from .models import Item, Order, ClientSecret


class HomePageView(TemplateView):
    template_name = 'home.html'


class ItemListView(ListView):
    model = Item
    template_name = 'items.html'
    context_object_name = 'items'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_info.html'


class OrderListView(ListView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order'


load_dotenv(find_dotenv())
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


# def chekout_session_create(self):
#     items = Order.objects.all()
#     order_price = 0
#     for i in items:
#         order_price += i.calculate_item_price()
#     print(order_price)
#     domain = 'http://localhost:8000'
#     session = stripe.checkout.Session.create(
#         line_items=[{
#             'price_data': {
#                 'currency': 'usd',
#                 'unit_amount': int(order_price) * 100,
#                 'product_data': {'name': 'order'},
#             },
#             'quantity': 1,
#         }],
#         mode='payment',
#         success_url=domain + '/success/',
#         cancel_url=domain + '/cancel/',
#     )
#     items.delete()
#     return JsonResponse({'id': session.id})

def payment_create(self):
    items = Order.objects.all()
    order_price = 0
    for i in items:
        order_price += i.calculate_item_price()
    customer_id = items[0].key.key
    print(order_price)
    session = stripe.PaymentIntent.create(
        amount=int(order_price),
        currency="usd",
        payment_method_types=["card"],
        customer=customer_id,
    )
    items.delete()
    ClientSecret.objects.all().delete()
    return JsonResponse({'session_id': session.id, 'price': session.amount, 'currency': session.currency})


def item_to_order(request, pk):
    try:
        secret = ClientSecret.objects.latest('key')
    except:
        secret = None
    if secret is None:
        session = stripe.Customer.create(
        )
        key = ClientSecret.objects.create(key=session.id)
        Order.objects.create(item_id=pk, key=key)
    else:
        Order.objects.create(item_id=pk, key=secret)
    messages.success(request, "Товар добавлен в корзину")
    return HttpResponseRedirect(reverse('items'))


def success_view(request):
    return render(request=request, template_name='success.html')


def cancel_view(request):
    return render(request=request, template_name='cancel.html')
