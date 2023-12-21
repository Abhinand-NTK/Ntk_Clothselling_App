# Generated by Django 4.2.4 on 2023-12-20 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0070_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Returned', 'Returned'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Return processing', 'Return processing'), ('Return requested', 'Return requested'), ('Out for delivery', 'Out for delivery'), ('Shipped', 'Shipped'), ('Order confirmed', 'Order confirmed')], default='Order Confirmed', max_length=50),
        ),
    ]
