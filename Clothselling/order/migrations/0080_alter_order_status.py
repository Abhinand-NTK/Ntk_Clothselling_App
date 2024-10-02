# Generated by Django 4.2.4 on 2023-12-27 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0079_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Order confirmed', 'Order confirmed'), ('Return requested', 'Return requested'), ('Cancelled', 'Cancelled'), ('Return processing', 'Return processing'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Returned', 'Returned')], default='Order Confirmed', max_length=50),
        ),
    ]
