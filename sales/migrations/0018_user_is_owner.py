# Generated by Django 3.1.2 on 2020-10-12 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0017_remove_sale_concessionaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_owner',
            field=models.BooleanField(default=False),
        ),
    ]
