# Generated by Django 3.2.5 on 2021-07-15 06:51

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_technology_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.JSONField()),
                ('descripiton', models.JSONField()),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('github', models.URLField()),
                ('link', models.URLField()),
                ('client', models.CharField(max_length=100)),
                ('duration', models.IntegerField()),
                ('technologies', models.ManyToManyField(to='core.Technology')),
            ],
        ),
    ]
