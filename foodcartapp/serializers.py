from rest_framework import serializers
from .models import Order
from .models import OrderDetails


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = ['quantity', 'product']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderDetailsSerializer(many=True, allow_empty=False, write_only=True)

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products']