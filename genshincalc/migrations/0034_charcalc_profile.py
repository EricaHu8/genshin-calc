# Generated by Django 5.1.3 on 2024-11-29 01:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genshincalc', '0033_profile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='charcalc',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='genshincalc.profile'),
            preserve_default=False,
        ),
    ]
