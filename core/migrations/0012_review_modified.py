# Generated by Django 3.2.2 on 2021-06-23 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_review_update_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='modified',
            field=models.BooleanField(default=False),
        ),
    ]
