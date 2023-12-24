# Generated by Django 5.0 on 2023-12-24 00:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripeapp', '0006_alter_order_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secret', to='stripeapp.clientsecret'),
        ),
    ]
