from rest_framework import generics
from rest_framework.response import Response
import json
from django.http import HttpResponse, JsonResponse

from lollipops.models import Courier
from lollipops.serializers import CourierDetailSerializer, CourierListSerializer


class CourierCreateView(generics.CreateAPIView):
    serializer_class = CourierDetailSerializer
    queryset = Courier.objects.all()

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data["data"], many=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        for i in range(len(ser.data)):
            del ser.data[i]['courier_type']
            del ser.data[i]['working_hours']
            del ser.data[i]['id']
            del ser.data[i]['regions']
            ser.data[i]['id'] = ser.data[i].pop('courier_id')
            values = {
                "courier": ser.data
            }

        return Response(values, status=201)



class CourierListView(generics.ListAPIView):
    serializer_class = CourierListSerializer
    queryset = Courier.objects.all()



class CourierDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = CourierDetailSerializer
    queryset = Courier.objects.all()
