from django.http import HttpResponseRedirect
from django import template
from django.shortcuts import render

from .models import Order

register = template.Library()

# @register.simple_tag(takes_context=True)
# def item_to_order(context, pk):
#     request = context['request']
#     Order.objects.create(item_id=pk)
#     return render(request=request, template_name='success.html')
