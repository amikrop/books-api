from django.conf import settings
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, blank=True)
    publication_date = models.DateField()
    comments_allowed = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
