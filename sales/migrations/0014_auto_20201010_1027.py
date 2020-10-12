# Generated by Django 3.1.2 on 2020-10-10 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0013_auto_20201009_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='activity1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='activity1', to='sales.activity'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='activity2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='activity2', to='sales.activity'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='activity3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='activity3', to='sales.activity'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='hotel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='hotel', to='sales.hotel'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='seller', to='sales.employee'),
        ),
    ]
