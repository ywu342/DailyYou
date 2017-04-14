from django.db import models

# Create your models here.
class Category(models.Model):
    cate_name = models.CharField(max_length=200,primary_key=True)
    
    def __str__(self):
        return self.cate_name
    
    class Meta:
        ordering = ('cate_name',)

class User(models.Model):
    username = models.CharField(max_length=200,primary_key=True)
    password = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    
    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ('username',)
