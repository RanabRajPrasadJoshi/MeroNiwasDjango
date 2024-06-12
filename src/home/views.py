from django.shortcuts import render , redirect
from django.http import HttpResponse
from . models import *

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def show_product(request):
    product = Product.objects.all()
    context = {
        'product':product
    }
    return render(request, 'home/index.html', context)

def show_contactus(request):
    return redirect(request, 'home/ContactUs.html')
