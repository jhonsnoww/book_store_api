from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250)
    eng_name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=250)
    eng_name = models.CharField(max_length=250, default=name)
    description = models.CharField(max_length=400, null=True)
    coverUrl = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=250)
    title_eng = models.CharField(max_length=250, default=title)
    authors = models.ManyToManyField(Author, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books')
    download_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    pdfFileUrl = models.CharField(max_length=250)
    coverUrl = models.CharField(max_length=250)

    class Meta:
        indexes = [
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return f'{self.title} by {", ".join(str(author) for author in self.authors.all())}'
