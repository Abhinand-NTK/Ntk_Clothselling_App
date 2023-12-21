# Generated by Django 4.2.4 on 2023-12-20 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0056_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Out for delivery', 'Out for delivery'), ('Return requested', 'Return requested'), ('Cancelled', 'Cancelled'), ('Return processing', 'Return processing'), ('Order confirmed', 'Order confirmed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Returned', 'Returned')], default='Order Confirmed', max_length=50),
        ),
    ]