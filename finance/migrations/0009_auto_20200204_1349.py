# Generated by Django 3.0.2 on 2020-02-04 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0008_auto_20200204_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trasaction',
            name='transaction_amount',
            field=models.IntegerField(),
        ),
    ]
