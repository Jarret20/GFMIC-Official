# Generated by Django 4.1.1 on 2023-02-22 13:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_certificate_cert_datecreated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='user_e_password',
            field=models.BinaryField(null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='cert_datecreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 13, 46, 15, 365535, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='cert_dateupdated',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 13, 46, 15, 365535, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_datecreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 13, 46, 15, 365535, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_dateupdated',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 13, 46, 15, 365535, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='membership',
            name='user_datecreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 13, 46, 15, 365535, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='membership',
            name='user_dateupdated',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 13, 46, 15, 365535, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='register_event',
            name='reg_payment_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 13, 46, 15, 365535, tzinfo=datetime.timezone.utc)),
        ),
    ]
