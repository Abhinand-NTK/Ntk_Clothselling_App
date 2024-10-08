# Generated by Django 4.2.4 on 2024-10-03 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0086_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order confirmed', 'Order confirmed'), ('Out for delivery', 'Out for delivery'), ('Returned', 'Returned'), ('Return requested', 'Return requested'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Return processing', 'Return processing')], default='Order Confirmed', max_length=50),
        ),
    ]
