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

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.name}: {self.price}'

    def get_absolute_url(self):
        return "/menu"

class RecipeRequirements(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    # def __str__(self):
    #     return f'{self.menu_item}, {self.ingredient}'

    def get_absolute_url(self):
        return '/menu'

class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return '/purchase'

    def get_cost(self):
        recipes = RecipeRequirements.objects.filter(menu_item=self.menu_item)
        return sum([i.ingredient.unit_price * i.quantity for i in recipes])

    def get_revenue(self):
        return self.menu_item.price

    def get_profit(self):
        return float(self.get_revenue()) - float(self.get_cost())
    