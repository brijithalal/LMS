# Generated by Django 5.1.3 on 2024-12-05 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_book_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='content_file',
            field=models.FileField(upload_to='library/books/', verbose_name='Book Content'),
        ),
    ]