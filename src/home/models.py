from django.db import models

# Create your models here.

class Categeory(models.Model):
    category_name = models.CharField(max_length=150)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField()
    img = models.FileField(upload_to='static/uploads')
    category = models.ForeignKey(Categeory, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.product_price)
