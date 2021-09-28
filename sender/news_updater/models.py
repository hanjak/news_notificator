from django.db import models

class Webnews(models.Model):
    text = models.CharField(max_length=150)
