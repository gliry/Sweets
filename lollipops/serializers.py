from rest_framework import serializers
from lollipops.models import Courier


class CourierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'


class CourierDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'
