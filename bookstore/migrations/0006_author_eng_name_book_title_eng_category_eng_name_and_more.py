# Generated by Django 4.2 on 2023-04-04 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0005_alter_book_authors_alter_book_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='eng_name',
            field=models.CharField(default=models.CharField(max_length=250), max_length=250),
        ),
        migrations.AddField(
            model_name='book',
            name='title_eng',
            field=models.CharField(default=models.CharField(max_length=250), max_length=250),
        ),
        migrations.AddField(
            model_name='category',
            name='eng_name',
            field=models.CharField(default=models.CharField(max_length=250), max_length=250),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]