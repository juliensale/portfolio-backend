# Generated by Django 3.2.2 on 2021-06-22 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_skill_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
