# Generated by Django 5.1.3 on 2024-12-08 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_alter_plancategory_category_alter_plancategory_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='rent_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
