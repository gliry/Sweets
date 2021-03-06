# Generated by Django 3.1.7 on 2021-03-29 15:12

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lollipops', '0008_courier_completed_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='completed_orders',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), blank=True, default=[], null=True, size=None),
        ),
    ]
