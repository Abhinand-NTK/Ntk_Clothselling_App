# Generated by Django 4.2.4 on 2023-09-21 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0004_wishlist_payementwallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='check_color',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
