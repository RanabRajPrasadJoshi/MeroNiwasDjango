from django.contrib import admin
from . models import * 

# Register your models here.
Category.objects.get_or_create(name='House')
Category.objects.get_or_create(name='Room')
Category.objects.get_or_create(name='Flat')
admin.site.register(Room)
admin.site.register(Category)
