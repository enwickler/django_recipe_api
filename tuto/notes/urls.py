from django.urls import path, include
from notes import views

urlpatterns = [
    path('recipes/',views.RecipeList.as_view()),
    path('recipes/<int:pk>/',views.RecipeDetail.as_view()),
    path('users/',views.UserList.as_view()),
    path('users/<int:pk>/',views.UserDetail.as_view()),
    path('api-auth/',include('rest_framework.urls')),
    path('recipes/<str:name>/',views.recipe_search),
    path('recipes/favorites/',views.RecipeFaveList.as_view())
]

