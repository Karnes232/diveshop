# Generated by Django 3.1.2 on 2020-10-08 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_user_hotel_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=120)),
                ('first_name', models.CharField(max_length=120)),
                ('id_number', models.CharField(max_length=120)),
                ('telephone', models.CharField(blank=True, max_length=10)),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
    ]
