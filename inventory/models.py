from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.FloatField(default=0)
    quantity_type = models.CharField(max_length=200)
    price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.name}: {self.quantity} ({self.quantity_type})'

    def get_absolute_url(self):
        return "/ingredients"

    def available(self):
        return self

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.name}: {self.price}'

    def available(self):
        return all(i.enough() for i in self.reciperequirements_set.all())

    def get_absolute_url(self):
        return "/menu"

class RecipeRequirements(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    def __str__(self):
        return f'{self.menu_item}, {self.ingredient}'

    def get_absolute_url(self):
        return '/recipe'

    def enough(self):
        return self.quantity <= self.ingredient.quantity

class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return "/purchase"

    def get_cost(self):
        recipe_objects = RecipeRequirements.objects.filter(menu_item=self.menu_item)
        return sum([i.ingredient.price * i.quantity for i in recipe_objects])

    def get_revenue(self):
        return self.menu_item.price

    def get_profit(self):
        return float(self.get_revenue()) - float(self.get_cost())