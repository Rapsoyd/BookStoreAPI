# Generated by Django 5.0.4 on 2024-05-05 10:09

import library.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=library.fields.WEBPField(blank=True, upload_to='products/%Y/%m/d'),
        ),
    ]