from django.contrib import admin
from . models import * 

# Register your models here.
Category.objects.get_or_create(name='HOME')
Category.objects.get_or_create(name='ROOM')
Category.objects.get_or_create(name='FLAT')
admin.site.register(Room)
admin.site.register(Category)
admin.site.register(UserProfile)
