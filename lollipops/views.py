import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from lollipops.models import Courier, Order
from lollipops.serializers import CourierDetailSerializer, CourierListSerializer, OrderDetailSerializer, \
    CourierAssignSerializer, OrderListSerializer, OrderAssignSerializer


class CourierCreateView(generics.CreateAPIView):
    serializer_class = CourierDetailSerializer
    queryset = Courier.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Make processing of POST-request for adding couriers in system. Available at the link couriers/.
        :param request: requesting data, json. Looks like {'data':[{courier1_params},{courier2_params}...]}
        :param args: unpacking arguments
        :param kwargs: unpacking named arguments
        :return: If couriers created returns HTTP 201 with list of imported courier ids.
        Else returns HTTP 400 Bad Request with list of validation error courier ids.
        """
        list_of_error_id = []
        ser_error = []
        ser_error_list_dict = []
        not_error = True  # Error flag

        # Getting serializer of request
        ser = self.get_serializer(data=request.data["data"], many=True)
        ser.is_valid(raise_exception=True)
        ser.save()

        for i in range(len(ser.data)):
            # Checking wrong params in request
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

            # Delete parameters that do not need to be output, rename courier_id to id, only for output
            del ser.data[i]['courier_type']
            del ser.data[i]['working_hours']
            del ser.data[i]['regions']
            del ser.data[i]['rating']
            del ser.data[i]['earnings']
            del ser.data[i]['order_id_delivery']
            ser.data[i]['id'] = ser.data[i].pop('courier_id')

        # preparing data for output
        for elem in list_of_error_id:
            ser_error.append(ser.data[elem])
            ser_error_list_dict.append(ser.data[elem]['id'])

        # delete accepted courier if it has invalid values
        for elem in ser_error_list_dict:
            Courier.objects.filter(courier_id=elem).delete()

        # output data describe
        added_couriers = {
            "couriers": ser.data
        }
        error_courier = {
            "validation_error": {
                "couriers": ser_error
            }
        }

        # return data with right status
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
        """
        Make processing of POST-request for allowing to change the information about the courier.
        Available at the link couriers/<int:pk>/, where <int:pk> is courier_id.

        :param request: requesting data, json. Looks like {courier_param: new_param, ...}
        :param pk: courier_id
        :return: If couriers params exist return HTTP 200 OK and actual information about courier.
        Else return HTTP 400 Bad Request
        """
        not_error = True  # error flag
        orders_weight = 0
        control_weight_error = True  # error flag
        counter = 0

        # for check updating of order_id_delivery is needed or not
        last_state_type = Courier.objects.filter(courier_id=pk)[0].courier_type

        # Getting serializer of request
        courier_object = self.get_object()
        serializer = CourierDetailSerializer(courier_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

        # Checking wrong params in request
        keys = request.data.keys()
        keys = list(keys)
        keys.remove('order_id_delivery')  # If order_id_delivery is empty it's OK
        for key in keys:
            if request.data[key] == '' or request.data[key] == [] or request.data[key] is None:
                not_error = False

        if Courier.objects.filter(courier_id=pk):  # if courier exist
            order_id_delivery = Courier.objects.filter(courier_id=pk)[0].order_id_delivery
            list_of_issued_orders = []
            order_data = list(Order.objects.all())
            length = len(order_data)

            # creating serializer data, parse it
            courier = Courier.objects.filter(courier_id=pk)[0]
            courier_data = CourierAssignSerializer(courier).data
            courier_working_hours = courier_data['working_hours']
            courier_regions = courier_data['regions']
            courier_type = courier_data['courier_type']

            if courier_type == 'foot':
                courier_weight = 10
            elif courier_type == 'bike':
                courier_weight = 15
            elif courier_type == 'car':
                courier_weight = 50

            while control_weight_error:
                for order in order_data:
                    counter += 1  # for interrupting loop

                    # parse order data
                    order_weight = order.weight
                    order_region = order.region
                    order_hours = order.delivery_hours
                    order_id = order.order_id
                    order_status = order.status

                    # checking  order status, conformity regions and time
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

                                        # removing iter-object if it fit at least one criterion
                                        if order in order_data:
                                            order_data.remove(order)

                                            # check weight overflow
                                            if orders_weight + order_weight <= courier_weight:
                                                orders_weight += order_weight
                                                list_of_issued_orders.append(order_id)
                    # break mechanism
                    if len(order_data) == 0:
                        control_weight_error = False
                # break mechanism
                if counter > length:
                    control_weight_error = False

        # when couriers parameters change, check difference in field order_id_delivery
        # with new field list_of_issued_orders, create list of different ids

        if order_id_delivery:
            difference = [i for i in order_id_delivery + list_of_issued_orders
                          if i not in order_id_delivery or i not in list_of_issued_orders]

            # For difference beetwen lists withdraw order, preparing right list_of_issued_orders
            for order_id in difference:
                Order.objects.filter(order_id=order_id).update(courier_id_delivery=-1, status='In processing',
                                                               assign_time='')
                if order_id in list_of_issued_orders:
                    list_of_issued_orders.remove(order_id)

        # changing data in order_id_delivery of order
        Courier.objects.filter(courier_id=pk).update(order_id_delivery=list_of_issued_orders)


        # return data with right status
        if not_error:
            return JsonResponse(status=201, data=serializer.data)
        else:
            return Response(status=400)

    def get(self, request, pk, *args, **kwargs):
        """
        Make processing of GET-request for present information about courier with new params.

        :param request:
        :param pk: courierd_id
        :param args: unpacking arguments
        :param kwargs: unpacking named arguments
        :return: courier's parameters with two additional params: rating and earnings.
        """
        list_of_all_regions = []
        list_of_delivery_times = []
        average_list = []
        orders_completed = Order.objects.filter(status='Completed')

        for order in orders_completed:
            list_of_all_regions.append(order.region)
        list_of_all_regions = list(set(list_of_all_regions))
        for region in list_of_all_regions:
            orders_completed_region = Order.objects.filter(status='Completed', region=region)
            for order in orders_completed_region:
                complete_time = datetime.datetime.strptime(order.complete_time[:-1], '%Y-%m-%dT%H:%M:%S.%f')
                assign_time = datetime.datetime.strptime(order.assign_time[:-1], '%Y-%m-%dT%H:%M:%S.%f')
                delivery_time_seconds = (complete_time - assign_time).total_seconds()
                list_of_delivery_times.append(delivery_time_seconds)
            average_list.append(sum(list_of_delivery_times) / len(orders_completed_region))
        average_min = min(average_list)

        rate = (60*60 - min(average_min, 60*60)) / (60*60) * 5
        earn = 0

        # creating serializer data
        courier_object = self.get_object()
        serializer = CourierDetailSerializer(courier_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

        # Updating data
        value = serializer.data
        value.update({'rating': rate})
        value.update({'earnings': earn})
        Courier.objects.filter(courier_id=pk).update(rating=rate, earnings=earn)

        # return data
        return Response(data=value)


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Make processing of POST-request for adding orders in system. Available at the link orders/.
        :param request: requesting data, json. Looks like {'data':[{order1_params},{order2_params}, ...]}
        :param args: unpacking arguments
        :param kwargs: unpacking named arguments
        :return: If orders created returns HTTP 201 with list of imported order ids.
        Else returns HTTP 400 Bad Request with list of validation error order ids.
        """
        list_of_error_id = []
        ser_error = []
        ser_error_list = []
        not_error = True

        # creating serializer data
        ser = self.get_serializer(data=request.data["data"], many=True)
        ser.is_valid(raise_exception=True)
        ser.save()

        for i in range(len(ser.data)):
            # Checking wrong params in request
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

            # Delete parameters that do not need to be output, rename order_id to id, only for output
            del ser.data[i]['weight']
            del ser.data[i]['region']
            del ser.data[i]['delivery_hours']
            del ser.data[i]['status']
            del ser.data[i]['assign_time']
            del ser.data[i]['complete_time']
            del ser.data[i]['courier_id_delivery']
            ser.data[i]['id'] = ser.data[i].pop('order_id')

        # preparing data for output
        for elem in list_of_error_id:
            ser_error.append(ser.data[elem])
            ser_error_list.append(ser.data[elem]['id'])

        # delete accepted order if it has invalid values
        for elem in ser_error_list:
            Order.objects.filter(order_id=elem).delete()

        # output data describe
        added_orders = {
            "orders": ser.data
        }
        error_order = {
            "validation_error": {
                "orders": ser_error
            }
        }

        # return data with right status
        if not_error:
            return Response(added_orders, status=201)
        else:
            return Response(error_order, status=400)


class OrderAssignView(generics.CreateAPIView):
    serializer_class = OrderAssignSerializer
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Make processing of POST-request for distribute orders to courier.
        Available at the link orders/assign/.
        :param request: requesting data, json. Looks like {'courier_id': courier_id}
        :param args: unpacking arguments
        :param kwargs: unpacking named arguments
        :return: If there are suitable orders, then return HTTP 200 OK and json like
        {"orders": [{"id": order_id1}, {"id": order_id2}, ...] "assign_time": "{time}" }.
        Else (if no matching orders) return empty list of orders withour returning assign_time.
        If courier doesn't exist return HTTP 400 Bad Request
        """
        list_of_issued_orders = []
        list_of_issued_ids = []
        orders_weight = 0
        control_weight_error = True
        counter = 0
        courier_id = request.data['courier_id']  # parse accepted data

        if Courier.objects.filter(courier_id=courier_id):  # if courier with courier_id exist

            # Getting object and serializer, parse data
            courier = get_object_or_404(Courier, pk=courier_id)
            courier_data = CourierAssignSerializer(courier).data
            courier_working_hours = courier_data['working_hours']
            courier_regions = courier_data['regions']
            courier_type = courier_data['courier_type']
            if courier_type == 'foot':
                courier_weight = 10
            elif courier_type == 'bike':
                courier_weight = 15
            elif courier_type == 'car':
                courier_weight = 50

            # represent orders data in list, save it len()
            order_data = list(Order.objects.all())
            length = len(order_data)

            while control_weight_error:
                for order in order_data:
                    counter += 1  # for interrupting loop

                    # parse order data
                    order_weight = order.weight
                    order_region = order.region
                    order_hours = order.delivery_hours
                    order_id = order.order_id
                    order_status = order.status
                    courier_id_delivery = order.courier_id_delivery

                    # checking  order status, conformity regions and time
                    if order_status == 'In processing' or (order_status == 'At courier'
                                                           and courier_id_delivery == courier_id):
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

                                        # removing iter-object if it fit at least one criterion
                                        if order in order_data:
                                            order_data.remove(order)

                                            # check weight overflow
                                            if orders_weight + order_weight <= courier_weight:
                                                orders_weight += order_weight
                                                list_of_issued_orders.append(order_id)
                    # break mechanism
                    if len(order_data) == 0:
                        control_weight_error = False
                # break mechanism
                if counter > length:
                    control_weight_error = False

            time = datetime.datetime.now().isoformat()
            # preparing data for output
            for elem in list_of_issued_orders:
                list_of_issued_ids.append({"id": elem})

                # Update order status
                if Order.objects.filter(order_id=elem)[0].status == 'In processing':
                    Order.objects.filter(order_id=elem).update(status='At courier', assign_time=f'{time}Z',
                                                               courier_id_delivery=courier_id)


                elif Order.objects.filter(order_id=elem)[0].status == 'Completed':
                    # removing completed orders from list
                    if elem in list_of_issued_ids:
                        list_of_issued_orders.remove(elem)

            # changing data in order_id_delivery of order
            Courier.objects.filter(courier_id=courier_id).update(order_id_delivery=list_of_issued_orders)

            # preparing data for output
            if list_of_issued_orders:
                data = {
                    "orders": list_of_issued_ids,
                    "assign_time": str(time)
                }
            else:
                data = {
                    "orders": list_of_issued_orders
                }

            # return data with right status
            return Response(data=data, status=200)
        else:
            return Response(status=400)


class OrderCompleteView(generics.CreateAPIView):
    serializer_class = OrderAssignSerializer
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Make processing of POST-request for mark as completed the order and write complete time.
        Available at the link orders/complete/.
        :param request: requesting data, json. Looks like {"courier_id": courier_id, "order_id": order_id,
        complete_time: "{time}" }
        :param args: unpacking arguments
        :param kwargs: unpacking named arguments
        :return: If courier and order exists return HTTP 200 OK with {"order_id": order_id}.
        Else return HTTP 400 Bad Request
        """
        # parse request data
        courier_id = request.data['courier_id']
        order_id = request.data['order_id']
        complete_time = request.data['complete_time']
        list_order_id_delivery = Courier.objects.filter(courier_id=courier_id)[0].order_id_delivery

        # Making status of order completed
        if Order.objects.filter(order_id=order_id) and Courier.objects.filter(courier_id=courier_id):
            if Order.objects.filter(courier_id_delivery=courier_id):
                if order_id in list_order_id_delivery:
                    list_order_id_delivery.remove(order_id)
                Order.objects.filter(order_id=order_id).update(status='Completed', complete_time=f'{complete_time}',)
                Courier.objects.filter(courier_id=courier_id).update(order_id_delivery=list_order_id_delivery)
                # preparing data for output
                data = {
                    "order_id": order_id
                }
                # return data with right status
                return Response(data=data, status=200)

        return Response(status=400)
