# Generated by Django 3.2.8 on 2021-11-09 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0004_alter_unpleasantcustomer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtypology',
            name='qty',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='qty'),
            preserve_default=False,
        ),
    ]
