from rest_framework import serializers
from lollipops.models import Courier, Order


class CourierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CourierDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'


class CourierAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'

class OrderAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

