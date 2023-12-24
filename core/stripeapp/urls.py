from django.urls import path, include

from .views import HomePageView, ItemListView, ItemDetailView, success_view, OrderListView, \
    item_to_order, payment_create

urlpatterns = [
    path('', ItemListView.as_view(), name='items'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item'),
    path('order/', OrderListView.as_view(), name='order'),
    path('to_order/<int:pk>/', item_to_order, name='item_to_order'),
    path('success/', success_view, name='success'),
    path('buy/', payment_create, name='stripe_buy'),
]
