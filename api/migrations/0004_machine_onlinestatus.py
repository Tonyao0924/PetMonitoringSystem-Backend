# Generated by Django 4.1.7 on 2023-03-27 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_machine_recordtype_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='onlineStatus',
            field=models.BooleanField(default=False),
        ),
    ]
