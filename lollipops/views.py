from rest_framework import generics

from lollipops.models import Courier
from lollipops.serializers import CourierDetailSerializer, CourierListSerializer


class CourierCreateView(generics.CreateAPIView):
    serializer_class = CourierDetailSerializer


class CourierListView(generics.ListAPIView):
    serializer_class = CourierListSerializer
    queryset = Courier.objects.all()


class CourierDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = CourierDetailSerializer
    queryset = Courier.objects.all()
