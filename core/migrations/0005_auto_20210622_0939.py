# Generated by Django 3.2.2 on 2021-06-22 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_skill_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='description',
            field=models.JSONField(default={'en': 'Test description', 'fr': 'Description de test'}),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.JSONField(),
        ),
    ]
