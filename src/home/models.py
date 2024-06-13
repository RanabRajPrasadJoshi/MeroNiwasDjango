from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Room(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    img = models.FileField(upload_to='uploads/')  # FileField for uploading images
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title