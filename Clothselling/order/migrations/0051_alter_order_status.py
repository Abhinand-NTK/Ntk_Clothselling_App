# Generated by Django 4.2.4 on 2023-12-19 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0050_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Out for delivery', 'Out for delivery'), ('Returned', 'Returned'), ('Return processing', 'Return processing'), ('Return requested', 'Return requested'), ('Order confirmed', 'Order confirmed'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled')], default='Order Confirmed', max_length=50),
        ),
    ]
