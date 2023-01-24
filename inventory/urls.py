from django.urls import path
from . import views
from django.contrib.auth import views as view


urlpatterns = [
    path('', views.home, name='home'),
    path('ingredients/', views.IngredientView.as_view(),name='ingredients'),
    path('ingredient/new', views.IngredientCreate.as_view(), name='create_ingredient'),
    path('ingredient/<pk>/update', views.IngredientUpdate.as_view(), name='update_ingredient'),
    path('ingredient/<pk>/delete', views.IngredientDelete.as_view(), name='delete_ingredient'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('menu/new', views.MenuCreate.as_view(), name='create_menu'),
    path('update/<pk>/menu/', views.MenuUpdate.as_view(), name='update_menu'),
    path('delete/<pk>/menu/', views.MenuDelete.as_view(), name='delete_menu'),
    path('recipe/', views.RecipeView.as_view(), name='recipe'),
    path('recipe/new', views.RecipeCreate.as_view(), name='create_recipe'),
    path('recipe/<pk>/update', views.RecipeUpdate.as_view(), name='update_recipe'),
    path('recipe/<pk>/delete', views.RecipeDelete.as_view(), name='delete_recipe'),
    path('purchase/', views.PurchaseView.as_view(), name='purchase'),
    path('purchase/new', views.PurchaseCreate.as_view(), name='create_purchase')
]