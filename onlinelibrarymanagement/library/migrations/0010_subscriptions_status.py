# Generated by Django 5.1.3 on 2024-12-10 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_alter_rent_rent_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptions',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Active'), (2, 'Expired')], default=2),
        ),
    ]
