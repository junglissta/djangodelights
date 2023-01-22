from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.FloatField(default=0)
    quantity_type = models.CharField(max_length=200)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name, self.quantity, self.quantity_type, self.price

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name, self.price

class RecipeRequirements(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    def __str__(self):
        return self.menu_item, self.ingredient

class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=0)
