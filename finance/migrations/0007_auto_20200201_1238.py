# Generated by Django 3.0.2 on 2020-02-01 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_trasaction_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trasaction',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.Profile'),
        ),
    ]