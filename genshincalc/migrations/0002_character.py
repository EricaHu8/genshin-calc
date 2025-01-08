# Generated by Django 5.1.3 on 2024-11-19 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genshincalc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('element', models.CharField(max_length=100)),
                ('rarity', models.IntegerField()),
                ('weapon_type', models.CharField(max_length=100)),
            ],
        ),
    ]
