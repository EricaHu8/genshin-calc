# Generated by Django 5.1.3 on 2024-11-25 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genshincalc', '0012_remove_weaponmapping_ascension_3_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ascension',
            fields=[
                ('level', models.IntegerField(primary_key=True, serialize=False)),
                ('gem_2', models.IntegerField()),
                ('gem_3', models.IntegerField()),
                ('gem_4', models.IntegerField()),
                ('gem_5', models.IntegerField()),
                ('item_1', models.IntegerField()),
                ('item_2', models.IntegerField()),
                ('item_3', models.IntegerField()),
                ('exp_2', models.IntegerField()),
                ('exp_3', models.IntegerField()),
                ('exp_4', models.IntegerField()),
                ('boss', models.IntegerField()),
                ('speciality', models.IntegerField()),
                ('mora', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='talent',
            name='id',
        ),
        migrations.AlterField(
            model_name='talent',
            name='level',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
