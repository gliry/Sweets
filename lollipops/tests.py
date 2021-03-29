from django.test import TestCase
import pytest
from lollipops.models import Courier, Order

class SweetTest(TestCase):

    def setUp(self):
        Courier.objects.create(courier_id=1, courier_type="foot",
                               regions=[1, 12, 22], working_hours=["11:35-14:05", "09:00-11:00"])
        Courier.objects.create(courier_id=2, courier_type="bike",
                               regions=[22], working_hours=["09:00-18:00"])
        Courier.objects.create(courier_id=3, courier_type="car",
                               regions=[23, 12, 22, 33], working_hours=["09:00-18:00"])

        Order.objects.create(order_id=1, weight=3, region=22, delivery_hours=["09:00-18:00"])
        Order.objects.create(order_id=2, weight=14, region=22, delivery_hours=["09:00-18:00"])
        Order.objects.create(order_id=3, weight=16, region=22, delivery_hours=["09:00-12:00", "16:00-21:30"])

    def test_sweet(self):
        courier_id_1_regions = Courier.objects.filter(courier_id=1)[0].regions
        courier_id_2_type = Courier.objects.filter(courier_id=2)[0].courier_type
        courier_id_3_delivery_hours = Courier.objects.filter(courier_id=3)[0].working_hours

        order_id_1_weight = Order.objects.filter(order_id=1)[0].weight
        order_id_2_region = Order.objects.filter(order_id=2)[0].region
        order_id_3_delivery_hours = Order.objects.filter(order_id=3)[0].delivery_hours

        self.assertEqual(courier_id_1_regions, [1, 12, 22])
        self.assertEqual(courier_id_2_type, "bike")
        self.assertEqual(courier_id_3_delivery_hours, ["09:00-18:00"])

        self.assertEqual(order_id_1_weight, 3)
        self.assertEqual(order_id_2_region, 22)
        self.assertEqual(order_id_3_delivery_hours, ["09:00-12:00", "16:00-21:30"])
