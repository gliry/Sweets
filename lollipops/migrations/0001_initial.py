# Generated by Django 3.1.7 on 2021-03-27 18:13

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('courier_id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('courier_type', models.CharField(blank=True, max_length=10)),
                ('regions', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), blank=True, null=True, size=None)),
                ('working_hours', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=64, null=True), blank=True, null=True, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('region', models.IntegerField(blank=True, null=True)),
                ('delivery_hours', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=64, null=True), blank=True, null=True, size=None)),
            ],
        ),
    ]
