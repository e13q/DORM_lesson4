# Generated by Django 3.1.14 on 2024-07-14 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0017_auto_20240714_0256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemon',
            old_name='pokemon_id',
            new_name='id',
        ),
    ]
