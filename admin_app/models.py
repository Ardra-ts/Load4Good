from django.db import models

# Create your models here.

class Charity(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='uploads/img')
    description = models.TextField()
    contact = models.CharField(max_length=100)
    