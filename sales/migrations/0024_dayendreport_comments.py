# Generated by Django 3.1.2 on 2020-10-14 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0023_dayendreport_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayendreport',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]