# Generated by Django 3.2.5 on 2021-07-18 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_project_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='review',
            name='message',
            field=models.TextField(blank=True, default=''),
        ),
    ]
