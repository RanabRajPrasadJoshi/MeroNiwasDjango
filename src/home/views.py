from django.shortcuts import render , redirect
from django.http import HttpResponse

from django.http import JsonResponse
from . models import *

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def show_product(request):
    return render(request, 'home/index.html')

def show_contactus(request):
    return render(request, 'home/ContactUs.html')

def search(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    rooms = Room.objects.all()
    
    if query:
        rooms = rooms.filter(description__icontains=query)
    
    if category:
        rooms = rooms.filter(category__name__icontains=category)

    categories = Category.objects.all()

    return render(request, 'home/Product.html', {'rooms': rooms, 'categories': categories})
