# Generated by Django 3.1.7 on 2021-03-23 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lollipops', '0004_auto_20210323_1241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courier',
            name='user',
        ),
    ]
