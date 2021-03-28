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
            del ser.data[i]['rating']
            del ser.data[i]['earnings']
            del ser.data[i]['order_id_delivery']
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
        if Courier.objects.filter(courier_id=pk):
            courier_id = pk
            courier_type = Courier.objects.filter(courier_id=pk)[0].courier_type
            regions = Courier.objects.filter(courier_id=pk)[0].regions
            working_hours = Courier.objects.filter(courier_id=pk)[0].working_hours
            order_id_delivery = Courier.objects.filter(courier_id=pk)[0].order_id_delivery

            list_of_issued_orders = []
            list_of_issued_ids = []

            courier = Courier.objects.filter(courier_id=pk)[0]
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
                    order_status = order.status

                    if order_status == 'In processing' or order_status == 'At courier':
                        if order_region in courier_regions:
                            for i in range(len(order_hours)):
                                for j in range(len(courier_working_hours)):
                                    if datetime.datetime.strptime(courier_working_hours[j].split('-')[0], '%H:%M') \
                                            <= datetime.datetime.strptime(order_hours[i].split('-')[0], '%H:%M') \
                                            < datetime.datetime.strptime(courier_working_hours[j].split('-')[1],
                                                                         '%H:%M') \
                                            or datetime.datetime.strptime(order_hours[i].split('-')[0], '%H:%M') \
                                            <= datetime.datetime.strptime(courier_working_hours[j].split('-')[0],
                                                                          '%H:%M') \
                                            < datetime.datetime.strptime(order_hours[i].split('-')[1], '%H:%M'):

                                        if order in order_data:
                                            order_data.remove(order)
                                            if orders_weight + order_weight <= courier_weight:
                                                orders_weight += order_weight
                                                list_of_issued_orders.append(order_id)

                if len(order_data) == 0:
                    control_weight_error = False
        if list_of_issued_orders != []:
            Courier.objects.filter(courier_id=pk).update(order_id_delivery=list_of_issued_orders)
        if order_id_delivery:
            difference = [x for x in order_id_delivery if x not in list_of_issued_orders]

            for order_id in difference:
                Order.objects.filter(order_id=order_id).update(courier_id_delivery=-1, status='In processing')

        if not_error:
            return JsonResponse(status=201, data=serializer.data)
        else:
            return Response(status=400)

    def get(self, request, *args, **kwargs):
        rate = 5
        earn = 10000
        courier_object = self.get_object()
        serializer = CourierDetailSerializer(courier_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        value = serializer.data
        value.update({'rating': rate})
        value.update({'earnings': earn})

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
            del ser.data[i]['status']
            del ser.data[i]['assign_time']
            del ser.data[i]['complete_time']
            del ser.data[i]['courier_id_delivery']
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
        if Courier.objects.filter(courier_id=courier_id):
            courier = get_object_or_404(Courier, pk=courier_id)
            courier_data = CourierAssignSerializer(courier).data

            order_data = list(Order.objects.all())
            length = len(order_data)

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
                    order_status = order.status

                    if order_status == 'In processing' or order_status == 'At courier':
                        if order_region in courier_regions:
                            print(order_region)
                            for i in range(len(order_hours)):
                                for j in range(len(courier_working_hours)):
                                    if datetime.datetime.strptime(courier_working_hours[j].split('-')[0], '%H:%M') \
                                            <= datetime.datetime.strptime(order_hours[i].split('-')[0], '%H:%M') \
                                            < datetime.datetime.strptime(courier_working_hours[j].split('-')[1],
                                                                         '%H:%M') \
                                            or datetime.datetime.strptime(order_hours[i].split('-')[0], '%H:%M') \
                                            <= datetime.datetime.strptime(courier_working_hours[j].split('-')[0],
                                                                          '%H:%M') \
                                            < datetime.datetime.strptime(order_hours[i].split('-')[1], '%H:%M'):
                                        orders_weight += order_weight

                                        if orders_weight <= courier_weight:

                                            if order in order_data:
                                                order_data.remove(order)

                                                list_of_issued_orders.append(order_id)
                                                print(list_of_issued_orders)

                                        else:
                                            control_weight_error = False
                    if len(order_data) == 0:
                        control_weight_error = False
                if counter > length:
                    control_weight_error = False

            time = datetime.datetime.now().isoformat()
            for elem in list_of_issued_orders:
                list_of_issued_ids.append({"id": elem})

                if Order.objects.filter(order_id=elem)[0].status == 'In processing':
                    Order.objects.filter(order_id=elem).update(status='At courier', assign_time=f'{time}Z',
                                                               courier_id_delivery=courier_id)

                elif Order.objects.filter(order_id=elem)[0].status == 'Completed':
                    if elem in list_of_issued_ids:
                        list_of_issued_orders.remove(elem)
            Courier.objects.filter(courier_id=courier_id).update(order_id_delivery=list_of_issued_orders)

            if list_of_issued_orders:
                data = {
                    "orders": list_of_issued_ids,
                    "assign_time": str(time)
                }
            else:
                data = {
                    "orders": list_of_issued_orders
                }

            return Response(data=data, status=200)
        else:
            return Response(status=400)


class OrderCompleteView(generics.CreateAPIView):
    serializer_class = OrderAssignSerializer
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        courier_id = request.data['courier_id']
        order_id = request.data['order_id']
        complete_time = request.data['complete_time']
        if Order.objects.filter(order_id=order_id):
            if Order.objects.filter(courier_id_delivery=courier_id):
                Order.objects.filter(order_id=order_id).update(status='Completed', complete_time=f'{complete_time}')
                data = {
                    "order_id": order_id
                }
                return Response(data=data, status=200)
        else:
            return Response(status=400)
