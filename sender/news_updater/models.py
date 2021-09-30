from django.db import models

class Webnews(models.Model):
    text = models.CharField(max_length=150)
    date = models.CharField(max_length=50,null=True)
    link = models.CharField(max_length=300,null=True)

