# Generated by Django 4.2.4 on 2023-12-20 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0074_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order confirmed', 'Order confirmed'), ('Return processing', 'Return processing'), ('Return requested', 'Return requested'), ('Returned', 'Returned'), ('Delivered', 'Delivered'), ('Out for delivery', 'Out for delivery'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled')], default='Order Confirmed', max_length=50),
        ),
    ]