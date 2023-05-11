import json

from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static

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


def register_order(request):
    try:
        data = json.loads(request.body.decode())

        first_name = data['firstname']
        last_name = data['lastname']
        phone_number = data['phonenumber']
        address = data['address']

        order = Order(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address
        )
        order.save()

        order_details_serializer = OrderDetailsSerializer(
            data=data['products'],
            many=True
        )
        order_details_serializer.is_valid(raise_exception=True)
        order_details_serializer.save(order=order)

        return JsonResponse({'message': 'Order created successfully'})
    except (
        KeyError,
        ValueError,
        Order.DoesNotExist,
        Product.DoesNotExist
    ) as error:
        return JsonResponse(error, status=400)


