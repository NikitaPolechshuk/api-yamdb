# Generated by Django 5.1.1 on 2025-07-10 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_genre_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['name'], 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
    ]
