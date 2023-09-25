# Generated by Django 4.2.4 on 2023-09-21 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order confirmed', 'Order confirmed'), ('Out for delivery', 'Out for delivery'), ('Returned', 'Returned'), ('Return requested', 'Return requested'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped'), ('Return processing', 'Return processing')], default='Order Confirmed', max_length=50),
        ),
    ]