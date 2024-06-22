from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import aauthenticate,login
from django.http import JsonResponse
from . models import *

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def show_product(request):
    return render(request, 'home/index.html')

def show_contactus(request):
    return render(request, 'home/ContactUs.html')
def show_successLogin(request):
    return render(request, 'home/LoginSuccess.html')

def show_selectRegister(request):
    return render(request, 'home/selectregister.html')

def show_login(request):

    if request.method =='POST':
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        if not email or not password:
            return HttpResponse("Please fill in all fields. Some fields are empty or only contain spaces.")
        user = aauthenticate(request, email=email , password=password)
        if user is not None:
            login(request,user)
            return HttpResponse("loggedin")
        else:
            return HttpResponse("error login")
    return render(request, 'home/login.html')


def show_registerBroker(request):

    if request.method == 'POST':
        uname = request.POST.get("username").strip()
        contact_number = request.POST.get("contactnumber").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        confirm_password = request.POST.get("confirm-password").strip()
        gender = request.POST.getlist("gender")
        profile_picture = request.FILES.get('profile-picture')
        Citizen_front = request.FILES.get('citizenship-front')
        Citizen_back = request.FILES.get('citizenship-back')
        accountType = "broker"

        if not uname or not contact_number or not email or not password or not confirm_password:
            return HttpResponse("Please fill in all fields. Some fields are empty or only contain spaces.")

        if password != confirm_password:
            return HttpResponse("Your password and confirm password must be the same.")

        if profile_picture:
            file_extension = profile_picture.name.split('.')[-1].lower()
            if file_extension not in ["jpg", "jpeg", "png", "gif"]:
                return HttpResponse("Please upload only image files (jpg, jpeg, png, gif).")
        if Citizen_front:
            file_extension = Citizen_front.name.split('.')[-1].lower()
            if file_extension not in ["jpg", "jpeg", "png", "gif"]:
                return HttpResponse("Please upload only image files (jpg, jpeg, png, gif).")
        if Citizen_back:
            file_extension = Citizen_back.name.split('.')[-1].lower()
            if file_extension not in ["jpg", "jpeg", "png", "gif"]:
                return HttpResponse("Please upload only image files (jpg, jpeg, png, gif).")

        user = User.objects.create_user(uname, email, password)
        user.save()

        profile = UserProfile(user=uname, contact_number=contact_number, email=email, password=password, gender=gender, profile_picture=profile_picture,Citizen_front= Citizen_front, Citizen_back=Citizen_back, accountType=accountType)
        profile.save()

        return redirect('/LoginSuccess')
        
    return render(request, 'home/registerbroker.html')

def show_registerRegular(request):
    if request.method == 'POST':
        uname = request.POST.get("username").strip()
        contact_number = request.POST.get("contactnumber").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        confirm_password = request.POST.get("confirm-password").strip()
        gender = request.POST.getlist("gender")
        profile_picture = request.FILES.get('profile-picture')
        accountType = "regular"

        if not uname or not contact_number or not email or not password or not confirm_password:
            return HttpResponse("Please fill in all fields. Some fields are empty or only contain spaces.")

        if password != confirm_password:
            return HttpResponse("Your password and confirm password must be the same.")

        if profile_picture:
            file_extension = profile_picture.name.split('.')[-1].lower()
            if file_extension not in ["jpg", "jpeg", "png", "gif"]:
                return HttpResponse("Please upload only image files (jpg, jpeg, png, gif).")

        user = User.objects.create_user(uname, email, password)
        user.save()

        profile = UserProfile(user=uname, contact_number=contact_number, email=email, password=password, gender=gender, profile_picture=profile_picture, accountType=accountType)
        profile.save()

        return redirect('/LoginSuccess')
        

    return render(request, 'home/registerregular.html')

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
