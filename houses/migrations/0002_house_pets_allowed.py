# Generated by Django 4.1.5 on 2023-04-19 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='pets_allowed',
            field=models.BooleanField(default=True),
        ),
    ]
