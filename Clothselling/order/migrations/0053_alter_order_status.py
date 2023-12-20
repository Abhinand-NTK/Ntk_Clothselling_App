# Generated by Django 4.2.4 on 2023-12-19 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0052_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Out for delivery', 'Out for delivery'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Return requested', 'Return requested'), ('Delivered', 'Delivered'), ('Returned', 'Returned'), ('Return processing', 'Return processing'), ('Order confirmed', 'Order confirmed')], default='Order Confirmed', max_length=50),
        ),
    ]
