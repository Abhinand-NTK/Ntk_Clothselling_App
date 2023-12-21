# Generated by Django 4.2.4 on 2023-12-20 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0071_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Return requested', 'Return requested'), ('Cancelled', 'Cancelled'), ('Out for delivery', 'Out for delivery'), ('Return processing', 'Return processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Order confirmed', 'Order confirmed'), ('Returned', 'Returned')], default='Order Confirmed', max_length=50),
        ),
    ]
