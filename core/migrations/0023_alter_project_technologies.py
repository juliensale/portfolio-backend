# Generated by Django 3.2.5 on 2021-07-31 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20210718_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='technologies',
            field=models.ManyToManyField(blank=True, to='core.Technology'),
        ),
    ]
