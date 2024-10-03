# Generated by Django 4.2.4 on 2024-01-11 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0082_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Order confirmed', 'Order confirmed'), ('Return processing', 'Return processing'), ('Return requested', 'Return requested'), ('Cancelled', 'Cancelled'), ('Out for delivery', 'Out for delivery'), ('Shipped', 'Shipped'), ('Returned', 'Returned')], default='Order Confirmed', max_length=50),
        ),
    ]