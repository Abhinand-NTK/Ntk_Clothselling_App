# Generated by Django 4.2.4 on 2023-12-19 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0041_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order confirmed', 'Order confirmed'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Out for delivery', 'Out for delivery'), ('Return requested', 'Return requested'), ('Returned', 'Returned'), ('Delivered', 'Delivered'), ('Return processing', 'Return processing')], default='Order Confirmed', max_length=50),
        ),
    ]