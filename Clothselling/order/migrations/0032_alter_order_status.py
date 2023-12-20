# Generated by Django 4.2.4 on 2023-12-18 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0031_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Returned', 'Returned'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Order confirmed', 'Order confirmed'), ('Delivered', 'Delivered'), ('Return requested', 'Return requested'), ('Out for delivery', 'Out for delivery'), ('Return processing', 'Return processing')], default='Order Confirmed', max_length=50),
        ),
    ]
