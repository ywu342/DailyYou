from django.db import models

# Create your models here.
class Category(models.Model):
    cate_name = models.CharField(max_length=200)

class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)

