from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Blog, Recipe, FavoriteRecipes
from django.contrib.auth.models import User
from .serializers import BlogSerializer, UserSerializer, RecipeSerializer, FavoriteRecipeSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view,permission_classes
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class BlogAPI(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.saver(owner=self.request.user)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

@api_view(['GET'])
def recipe_search(request,name):
    if request.method == 'GET':
        recipe_by_search = Recipe.objects.filter(title__icontains=name)
        serializer = RecipeSerializer(recipe_by_search, many=True)
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_recipes(request,name):
    if request.method == 'GET':
        favorites = FavoriteRecipes.objects.filter(user=request.user)
        serializer = FavoriteRecipeSerializer(favorites,many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = FavoriteRecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeFaveList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)