# Generated by Django 4.2 on 2023-04-24 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='photo',
        ),
    ]
