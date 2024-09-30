from django.conf import settings
from django.db import models


class Comment(models.Model):
    content = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
