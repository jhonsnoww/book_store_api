# Generated by Django 4.2 on 2023-04-18 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_favorite'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]