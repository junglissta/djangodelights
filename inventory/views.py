from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Sum, F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import SuspiciousOperation
from .models import Ingredient, MenuItem, Purchase, RecipeRequirements
from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm, PurchaseForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/home.html"

class IngredientView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = 'inventory/ingredients.html'

class IngredientCreate(LoginRequiredMixin, CreateView):
    template_name = 'inventory/add_ingredient.html'
    model = Ingredient
    form_class = IngredientForm

class IngredientUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/update_ingredient.html'
    form_class = IngredientForm
    model = Ingredient

class IngredientDelete(LoginRequiredMixin, DeleteView):
    template_name = 'inventory/delete_ingredient.html'
    model = Ingredient
    success_url = '/ingredients'


class MenuView(LoginRequiredMixin, ListView):
    template_name = 'inventory/menu.html'
    model = MenuItem

class MenuCreate(LoginRequiredMixin, CreateView):
    template_name = 'inventory/add_menu.html'
    model = MenuItem
    form_class = MenuItemForm

class MenuUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/update_menu.html'
    form_class = MenuItemForm
    model = MenuItem

class MenuDelete(LoginRequiredMixin, DeleteView):
    template_name = 'inventory/delete_menu'
    model = MenuItem
    success_url = '/menu'

class RecipeView(LoginRequiredMixin, ListView):
    template_name = 'inventory/recipe.html'
    model = RecipeRequirements

class RecipeCreate(LoginRequiredMixin, CreateView):
    template_name = 'inventory/add_recipe.html'
    model = RecipeRequirements
    form_class = RecipeRequirementForm

class RecipeUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/update_recipe.html'
    model = RecipeRequirements
    form_class = RecipeRequirementForm

class RecipeDelete(LoginRequiredMixin, DeleteView):
    template_name = 'inventory/delete_recipe.html'
    success_url = '/'

class PurchaseView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'inventory/purchase.html'

class PurchaseCreate(LoginRequiredMixin, CreateView):
    template_name = 'inventory/add_purchase.html'
    model = Purchase
    form_class = PurchaseForm

def signout(request):
    logout(request)
    return redirect('/')