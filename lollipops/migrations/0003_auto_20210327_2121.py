# Generated by Django 3.1.7 on 2021-03-27 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lollipops', '0002_auto_20210327_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
