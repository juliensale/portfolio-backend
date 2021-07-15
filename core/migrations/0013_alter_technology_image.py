# Generated by Django 3.2.5 on 2021-07-14 09:27

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_review_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technology',
            name='image',
            field=cloudinary.models.CloudinaryField(default=None, max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
    ]
