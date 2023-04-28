# Generated by Django 4.2 on 2023-04-28 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='custom_game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platforms', models.CharField(choices=[('platform_1', 'platform_1'), ('platform_2', 'platform_2'), ('platform_3', 'platform_3')], max_length=10)),
                ('backgrounds', models.CharField(choices=[('background_1', 'background_1'), ('background_2', 'background_2'), ('background_3', 'background_3')], max_length=12)),
                ('obstacle', models.CharField(choices=[('obstacle_1', 'obstacle_1'), ('obstacle_2', 'obstacle_2'), ('obstacle_3', 'obstacle_3')], max_length=10)),
            ],
        ),
    ]