# Generated by Django 4.2.3 on 2024-09-26 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=500, null=True)),
                ('challenge', models.CharField(blank=True, max_length=500, null=True)),
                ('type', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
