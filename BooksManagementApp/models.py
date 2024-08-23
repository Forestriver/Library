from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(max_length=20, unique=True)
    pages = models.IntegerField(blank=True, null=True)
    cover = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.title)
