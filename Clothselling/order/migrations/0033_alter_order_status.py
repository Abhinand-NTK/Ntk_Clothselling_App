# Generated by Django 4.2.4 on 2023-12-18 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0032_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Returned', 'Returned'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Return processing', 'Return processing'), ('Order confirmed', 'Order confirmed'), ('Out for delivery', 'Out for delivery'), ('Return requested', 'Return requested'), ('Shipped', 'Shipped')], default='Order Confirmed', max_length=50),
        ),
    ]
