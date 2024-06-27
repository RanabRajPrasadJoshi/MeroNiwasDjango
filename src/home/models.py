from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    CATEGOTY = (
        ('HOME','HOME'),
        ('FLAT', 'FLAT'),
        ('ROOM', 'ROOM')
    )
    name = models.CharField(choices=CATEGOTY, max_length=250)

    def __str__(self):
        return self.name

class Room(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    img = models.FileField(upload_to='static/uploads')  # FileField for uploading images
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.CharField(default="null" , max_length=255, null=False)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.CharField(max_length=255, null=False)
    contact_number = models.CharField(max_length=15, null=False)
    email = models.EmailField(max_length=254, null=False)
    gender = models.CharField(max_length=10, null=False)
    profile_picture = models.ImageField(upload_to='static/uploadProfile', blank=True, null=True)
    Citizen_front = models.ImageField(upload_to='static/UploadCitizen', blank=True, null=True)
    Citizen_back = models.ImageField(upload_to='static/UploadCitizen', blank=True, null=True)
    accountType = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.user