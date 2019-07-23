# Generated by Django 2.0 on 2019-07-23 08:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0006_remove_fdata_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='fdata',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
