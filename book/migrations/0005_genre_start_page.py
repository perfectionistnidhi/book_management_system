# Generated by Django 5.1.5 on 2025-01-20 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_remove_book_url_alter_book_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='start_page',
            field=models.IntegerField(default=1),
        ),
    ]
