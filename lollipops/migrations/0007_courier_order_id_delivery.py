# Generated by Django 3.1.7 on 2021-03-27 22:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lollipops', '0006_order_courier_id_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='courier',
            name='order_id_delivery',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), blank=True, null=True, size=None),
        ),
    ]
