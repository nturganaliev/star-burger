from rest_framework import serializers
from .models import OrderDetails


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = ['product', 'quantity']

    def validate_product(self, value):
        if value is None:
            raise serializers.ValidationError("Product cannot be null.")
        return value