# Generated by Django 4.2.4 on 2023-09-02 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_auth', '0013_alter_coupons_maximum_order_amount_the_discount_percenetage_applicable_for'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupons',
            name='coupon_code',
            field=models.CharField(default=None, max_length=20, unique=True),
        ),
    ]