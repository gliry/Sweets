# Generated by Django 3.1.7 on 2021-03-22 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lollipops', '0002_auto_20210322_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='regions',
            field=models.CharField(db_index=True, max_length=64, verbose_name='regions'),
        ),
        migrations.AlterField(
            model_name='courier',
            name='working_hours',
            field=models.CharField(max_length=64, verbose_name='working_hours'),
        ),
    ]
