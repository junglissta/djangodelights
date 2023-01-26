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
    template_name = 'inventory/delete_menu.html'
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
    model = RecipeRequirements
    success_url = '/recipe'

class PurchaseView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'inventory/purchase.html'

class PurchaseCreate(LoginRequiredMixin, TemplateView):
    template_name = "inventory/add_purchase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = [i for i in MenuItem.objects.all() if i.available()]
        return context

    def post(self, request):
        menu_item_id = request.POST["menu_item"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirements_set
        purchase = Purchase(menu_item=menu_item)

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.quantity -= requirement.quantity
            required_ingredient.save()

        purchase.save()
        return redirect("/purchase")

class PurchaseDelete(LoginRequiredMixin, DeleteView):
    template_name = 'inventory/delete_purchase.html'
    model = Purchase
    success_url = '/purchase'

class FinanceView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/finance.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cost'] = round(sum([p.get_cost() for p in Purchase.objects.all()]), 2)
        context['revenue'] = round(sum([p.get_revenue() for p in Purchase.objects.all()]), 2)
        context['profit'] = round(sum([p.get_profit() for p in Purchase.objects.all()]), 2)
        

        return context



class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["purchases"] = Purchase.objects.all()
        revenue = Purchase.objects.aggregate(
            revenue=Sum("menu_item__price"))["revenue"]
        total_cost = 0
        for purchase in Purchase.objects.all():
            for recipe_requirement in purchase.menu_item.reciperequirement_set.all():
                total_cost += recipe_requirement.ingredient.price_per_unit * \
                    recipe_requirement.quantity

        context["revenue"] = revenue
        context["total_cost"] = total_cost
        context["profit"] = revenue - total_cost

        return context



def signout(request):
    logout(request)
    return redirect('/')