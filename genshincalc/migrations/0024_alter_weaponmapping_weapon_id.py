# Generated by Django 5.1.3 on 2024-11-28 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genshincalc', '0023_rename_character_id_id_charactermapping_character_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weaponmapping',
            name='weapon_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='genshincalc.weapon'),
        ),
    ]
