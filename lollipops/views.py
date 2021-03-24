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
        list_of_error_id = []
        ser_error = []
        not_error = True
        ser = self.get_serializer(data=request.data["data"], many=True)
        ser.is_valid(raise_exception=True)
        ser.save()

        for i in range(len(ser.data)):
            if ser.data[i]['courier_type'] == '':
                list_of_error_id.append(i)
                not_error = False
            elif ser.data[i]['working_hours'] == [''] or ser.data[i]['working_hours'] == [] \
                    or ser.data[i]['working_hours'] is None:
                list_of_error_id.append(i)
                not_error = False
            elif ser.data[i]['regions'] == [] or ser.data[i]['regions'] is None:
                list_of_error_id.append(i)
                not_error = False
            del ser.data[i]['courier_type']
            del ser.data[i]['working_hours']
            del ser.data[i]['id']
            del ser.data[i]['regions']
            ser.data[i]['id'] = ser.data[i].pop('courier_id')

        for elem in list_of_error_id:
            ser_error.append(ser.data[elem])

        added_couriers = {
            "courier": ser.data
        }
        error_courier = {
            "validation_error": {
                "courier": ser_error
            }
        }
        if not_error:
            return Response(added_couriers, status=201)
        else:
            return Response(error_courier, status=400)


class CourierListView(generics.ListAPIView):
    serializer_class = CourierListSerializer
    queryset = Courier.objects.all()


class CourierDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = CourierDetailSerializer
    queryset = Courier.objects.all()
