from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Blog(models.Model):
    author = models.ForeignKey(User, related_name='blogs', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class Recipe(models.Model):
    owner = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.URLField(max_length=2400)
    created = models.DateTimeField(auto_now_add=True)

class FavoriteRecipes(models.Model):
    user = models.ForeignKey(User,unique=False, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,unique=False, on_delete=models.CASCADE)