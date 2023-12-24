from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item')
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey('Tax', on_delete=models.SET_NULL, null=True, blank=True)
    key = models.ForeignKey('ClientSecret', on_delete=models.CASCADE, null=True, blank=True, related_name='secret')

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.tax_id = 1
        self.discount_id = 2

    def calculate_item_price(self):
        item_price = float(self.item.price)
        if self.discount:
            discount_amount = (self.discount.discount_percent / 100) * item_price
            item_price -= discount_amount
        if self.tax:
            tax_amount = (self.tax.tax_percent / 100) * item_price
            item_price += tax_amount
        return item_price


class Discount(models.Model):
    discount_percent = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])


class Tax(models.Model):
    tax_percent = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])


class ClientSecret(models.Model):
    key = models.CharField(max_length=255)
