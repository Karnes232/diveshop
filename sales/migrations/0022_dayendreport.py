# Generated by Django 3.1.2 on 2020-10-14 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0021_emaillist'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayEndReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gasoline', models.IntegerField()),
                ('usd', models.IntegerField()),
                ('cdn', models.IntegerField()),
                ('rd', models.IntegerField()),
                ('euro', models.IntegerField()),
                ('visa', models.IntegerField()),
                ('master_card', models.IntegerField()),
                ('amex', models.IntegerField()),
                ('office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dayend_office', to='sales.office')),
            ],
        ),
    ]
