# Generated by Django 3.0.2 on 2020-02-01 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_auto_20200201_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='trasaction',
            name='profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.Profile'),
        ),
    ]
