# Generated by Django 4.2.4 on 2023-09-20 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_auth', '0016_alter_banner_link_alter_banner_linkfordata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='linkfordata',
            field=models.CharField(blank=True, null=True),
        ),
    ]
