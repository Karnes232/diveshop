# Generated by Django 3.1.2 on 2020-10-11 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0015_auto_20201010_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='concessionaire',
            field=models.BooleanField(default=False),
        ),
    ]