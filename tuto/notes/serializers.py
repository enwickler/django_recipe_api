from rest_framework import serializers
from .models import Blog, Recipe, FavoriteRecipes
from django.contrib.auth.models import User

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','title','body']

class UserSerializer(serializers.ModelSerializer):
    recipes = serializers.PrimaryKeyRelatedField(many=True, queryset=Recipe.objects.all())
    
    class Meta:
        model = User
        fields = ['id','username','recipes']

class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Recipe
        fields = ['id','title','body','created','owner','image']


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class meta:
        model = FavoriteRecipes
        fields = ['id','recipe']