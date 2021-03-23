# Generated by Django 3.1.7 on 2021-03-23 09:41

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lollipops', '0003_auto_20210322_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='courier_id',
            field=models.PositiveIntegerField(db_index=True, unique=True, verbose_name='courier_id'),
        ),
        migrations.AlterField(
            model_name='courier',
            name='courier_type',
            field=models.CharField(max_length=10, verbose_name='courier_type'),
        ),
        migrations.AlterField(
            model_name='courier',
            name='regions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='courier',
            name='working_hours',
            field=models.CharField(max_length=128, verbose_name='working_hours'),
        ),
    ]
