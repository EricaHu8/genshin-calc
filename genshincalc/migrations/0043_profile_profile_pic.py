# Generated by Django 5.1.3 on 2024-11-30 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genshincalc', '0042_remove_exp_rarity_remove_gem_rarity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
