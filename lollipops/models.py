from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from ast import literal_eval

User = get_user_model()


class Courier(models.Model):
    courier_id = models.PositiveIntegerField(verbose_name='courier_id', db_index=True, unique=True)
    courier_type = models.CharField(verbose_name='courier_type', max_length=10)
    regions = ArrayField(models.IntegerField(), blank=True, null=True)
    working_hours = models.CharField(verbose_name='working_hours', max_length=128)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
