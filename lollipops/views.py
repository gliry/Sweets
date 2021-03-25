from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse

from lollipops.models import Courier, Order
from lollipops.serializers import CourierDetailSerializer, CourierListSerializer, OrderDetailSerializer, \
    OrderAssignSerializer, OrderListSerializer


class CourierCreateView(generics.CreateAPIView):
    serializer_class = CourierDetailSerializer
    queryset = Courier.objects.all()

    def post(self, request, *args, **kwargs):
        list_of_error_id = []
        ser_error = []
        ser_error_list = []
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
            del ser.data[i]['regions']
            ser.data[i]['id'] = ser.data[i].pop('courier_id')

        for elem in list_of_error_id:
            ser_error.append(ser.data[elem])
            ser_error_list.append(ser.data[elem]['id'])

        for elem in ser_error_list:
            Courier.objects.filter(courier_id=elem).delete()

        added_couriers = {
            "couriers": ser.data
        }
        error_courier = {
            "validation_error": {
                "couriers": ser_error
            }
        }
        if not_error:
            return Response(added_couriers, status=201)
        else:
            return Response(error_courier, status=400)


class CourierListView(generics.ListAPIView):
    serializer_class = CourierListSerializer
    queryset = Courier.objects.all()


class OrderListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()


class CourierDetailView(generics.RetrieveDestroyAPIView, generics.ListAPIView):
    serializer_class = CourierDetailSerializer
    queryset = Courier.objects.all()

    def patch(self, request):
        not_error = True
        courier_object = self.get_object()
        serializer = CourierDetailSerializer(courier_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        keys = request.data.keys()
        for key in keys:
            if request.data[key] == '' or request.data[key] == [] or request.data[key] is None:
                not_error = False

        if not_error:
            return JsonResponse(status=201, data=serializer.data)
        else:
            return Response(status=400)

    def get(self, request, *args, **kwargs):
        rating = 5
        earnings = 10000
        courier_object = self.get_object()
        serializer = CourierDetailSerializer(courier_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        value = serializer.data
        value.update({'rating': rating})
        value.update({'earnings': earnings})

        return Response(data=value)


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        list_of_error_id = []
        ser_error = []
        ser_error_list = []
        not_error = True
        ser = self.get_serializer(data=request.data["data"], many=True)
        ser.is_valid(raise_exception=True)
        ser.save()

        for i in range(len(ser.data)):
            if ser.data[i]['order_id'] is None:
                list_of_error_id.append(i)
                not_error = False
            elif ser.data[i]['weight'] is None:
                list_of_error_id.append(i)
                not_error = False
            elif ser.data[i]['region'] is None:
                list_of_error_id.append(i)
                not_error = False
            elif ser.data[i]['delivery_hours'] == [''] or ser.data[i]['delivery_hours'] == [] \
                    or ser.data[i]['delivery_hours'] is None:
                list_of_error_id.append(i)
                not_error = False

            del ser.data[i]['weight']
            del ser.data[i]['region']
            del ser.data[i]['delivery_hours']
            ser.data[i]['id'] = ser.data[i].pop('order_id')

        for elem in list_of_error_id:
            ser_error.append(ser.data[elem])
            ser_error_list.append(ser.data[elem]['id'])

        for elem in ser_error_list:
            Order.objects.filter(order_id=elem).delete()

        added_orders = {
            "orders": ser.data
        }
        error_order = {
            "validation_error": {
                "orders": ser_error
            }
        }
        if not_error:
            return Response(added_orders, status=201)
        else:
            return Response(error_order, status=400)


class OrderAssignView(generics.CreateAPIView):
    serializer_class = OrderAssignSerializer
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        courier_id = request.data['courier_id']
        courier = get_object_or_404(Courier, pk=courier_id)
        data = OrderAssignSerializer(courier).data
        return Response(data=data)
