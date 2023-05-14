import json
import re

from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import OrderDetailsSerializer
from .models import Order
from .models import Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    data = request.data
    print(data)

    if not isinstance(
        data.get('products'), list) or not data.get('products'):
            return Response("'products' must be non-empty list.")
    if not isinstance(
        data.get('firstname'), str) or not data.get('firstname'):
            return Response("'firstname' must be non-empty string.")
    if not isinstance(data.get('lastname'), str):
        return Response("'lastname' must be string.")
    if not re.match(r'\+79\d{9}$', data.get('phonenumber')):
        return Response("'phonenumber' must be non-empty string"\
            "and must startswith +79... length should be 10 digits.")
    if not isinstance(data.get('address'), str) or not data.get('address'):
        return Response("'address' must be non-empty string")

    order_details_serializer = OrderDetailsSerializer(
        data=data['products'],
        many=True
    )
    order_details_serializer.is_valid(raise_exception=True)

    order = Order(
        first_name=data['firstname'],
        last_name=data['lastname'],
        phone_number=data['phonenumber'],
        address=data['address']
    )
    order.save()

    order_details_serializer.save(order=order)

    return Response(data)
