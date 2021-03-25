from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from ast import literal_eval


class Courier(models.Model):
    courier_id = models.PositiveIntegerField(unique=True, primary_key=True)
    courier_type = models.CharField(max_length=10, blank=True)
    regions = ArrayField(models.IntegerField(blank=True, null=True), blank=True, null=True)
    working_hours = ArrayField(models.CharField(max_length=128, blank=True, null=True), blank=True, null=True)


class Order(models.Model):
    order_id = models.PositiveIntegerField(unique=True, primary_key=True)
    weight = models.FloatField(blank=True, null=True)
    region = models.IntegerField(blank=True, null=True)
    delivery_hours = ArrayField(models.CharField(max_length=128, blank=True, null=True), blank=True, null=True)


