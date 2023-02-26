from django.db import models
from django.conf import settings

class Note(models.Model):

    title = models.CharField(max_length = 200)
    body = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 
    def __str__(self):
        return self.title
