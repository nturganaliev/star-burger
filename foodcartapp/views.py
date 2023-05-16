import json

from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from .serializers import OrderDetailsSerializer
from .serializers import OrderSerializer
from .models import Order
from .models import OrderDetails
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


@api_view(['POST', ])
@transaction.atomic
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    order = Order.objects.create(
        lastname=validated_data['lastname'],
        firstname=validated_data['firstname'],
        phonenumber=validated_data['phonenumber'],
        address=validated_data['address']
    )

    order_items_fields = validated_data.get('products')
    print(order_items_fields)
    order_items = [
        OrderDetails(
            order=order,
            price=fields.get('product').price * fields.get('quantity'),
            **fields,
        ) for fields in order_items_fields
    ]

    OrderDetails.objects.bulk_create(order_items)
    serializer = OrderSerializer(order)

    return Response(serializer.data)