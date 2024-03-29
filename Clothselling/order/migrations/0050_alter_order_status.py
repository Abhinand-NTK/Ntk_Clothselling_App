# Generated by Django 4.2.4 on 2023-12-19 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0049_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Order confirmed', 'Order confirmed'), ('Return requested', 'Return requested'), ('Return processing', 'Return processing'), ('Returned', 'Returned'), ('Shipped', 'Shipped'), ('Out for delivery', 'Out for delivery')], default='Order Confirmed', max_length=50),
        ),
    ]
