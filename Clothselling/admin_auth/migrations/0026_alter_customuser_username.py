# Generated by Django 4.2.4 on 2024-10-03 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_auth', '0025_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]