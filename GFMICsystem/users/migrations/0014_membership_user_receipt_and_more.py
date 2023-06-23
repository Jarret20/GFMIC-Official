# Generated by Django 4.1.1 on 2023-03-03 12:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_register_event_reg_ecert_no_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='user_receipt',
            field=models.CharField(max_length=15, null=True, unique=True, verbose_name='Official Receipt Number'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='cert_datecreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 12, 23, 19, 639693, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='cert_dateupdated',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 12, 23, 19, 639693, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_datecreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 12, 23, 19, 639693, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_dateupdated',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 12, 23, 19, 639693, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='membership',
            name='user_datecreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 12, 23, 19, 639693, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='membership',
            name='user_dateupdated',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 12, 23, 19, 639693, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='register_event',
            name='reg_payment_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 12, 23, 19, 639693, tzinfo=datetime.timezone.utc)),
        ),
    ]
