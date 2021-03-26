from xmlrpc.client import DateTime

from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from lollipops.models import Courier, Order
from lollipops.serializers import CourierDetailSerializer, CourierListSerializer, OrderDetailSerializer, \
    CourierAssignSerializer, OrderListSerializer, OrderAssignSerializer
import datetime


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

    def patch(self, request, pk):
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
            if ser.data[i]['weight'] > 50 or ser.data[i]['weight'] < 0.01:
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
        list_of_issued_orders = []
        list_of_issued_ids = []
        courier_id = request.data['courier_id']
        courier = get_object_or_404(Courier, pk=courier_id)
        courier_data = CourierAssignSerializer(courier).data

        order_data = list(Order.objects.all())

        courier_working_hours = courier_data['working_hours']
        courier_regions = courier_data['regions']
        courier_type = courier_data['courier_type']
        if courier_type == 'foot':
            courier_weight = 10
        elif courier_type == 'bike':
            courier_weight = 15
        elif courier_type == 'car':
            courier_weight = 50
        orders_weight = 0
        control_weight_error = True
        counter = 0
        while control_weight_error:
            for order in order_data:
                counter += 1
                order_weight = order.weight
                order_region = order.region
                order_hours = order.delivery_hours
                order_id = order.order_id

                if order_region in courier_regions:
                    for i in range(len(order_hours)):
                        for j in range(len(courier_working_hours)):
                            if datetime.datetime.strptime(courier_working_hours[j].split('-')[0], '%H:%M') \
                                    < datetime.datetime.strptime(order_hours[i].split('-')[0], '%H:%M') \
                                    < datetime.datetime.strptime(courier_working_hours[j].split('-')[1], '%H:%M') \
                                    or datetime.datetime.strptime(order_hours[i].split('-')[0], '%H:%M') \
                                    < datetime.datetime.strptime(courier_working_hours[j].split('-')[0], '%H:%M') \
                                    < datetime.datetime.strptime(order_hours[i].split('-')[1], '%H:%M'):

                                orders_weight += order_weight
                                if orders_weight <= courier_weight:
                                    list_of_issued_orders.append(order_id)
                                    order_data.remove(order)
                                else:
                                    control_weight_error = False
                if counter > len(order_data):
                    control_weight_error = False

        print(set(list_of_issued_orders))
        print(orders_weight)
        for elem in list_of_issued_orders:
            list_of_issued_ids.append({"id": elem})
        time = datetime.datetime.now()
        if list_of_issued_orders:
            data = {
                "orders": list_of_issued_orders,
                "assign_time": str(time) + "Z"
            }
        else:
            data = {
                "orders": list_of_issued_orders
            }

        return Response(data=data)


class OrderCompleteView(generics.CreateAPIView):
    serializer_class = OrderAssignSerializer
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        courier_id = request.data['courier_id']
        order_id = request.data['order_id']
        complete_time = datetime.datetime.now()

        data = {
            "order_id": order_id
        }
        return Response(data=data)