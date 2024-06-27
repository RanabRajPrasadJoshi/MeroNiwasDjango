from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from . models import *
import random
from django.core.mail import send_mail
from django.conf import settings

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
        try:
            user_profileEmail = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return HttpResponse("No user with this email address exists.")
        user = authenticate(request, username=user_profileEmail.user , password=password)
        if user is not None:
            login(request,user)
            user_profile = UserProfile.objects.get(user=user) 
            if user_profile.accountType == "regular":
                return redirect("/")
            if user_profile.accountType == "broker":
                return redirect('/Product')
            else:
                return HttpResponse("Error login")
        else:
            return HttpResponse("Email or Password Incorrect")
    return render(request, 'home/login.html')

def show_logout(request):
    logout(request)
    return redirect('/')


def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(email, code , username):
    subject = "Welcome to Mero Niwas - Verify Your Email"
    message = f"Dear {username} ,Greetings from Mero Niwas! We're delighted to have you on board as part of our community, where finding your ideal home or room for rent is just a few clicks away.\n \n Once verified, you'll gain access to a wide range of rental options tailored to your preferences. Whether it's a cozy apartment or a spacious house, we've got you covered.\n \n Your Verification Code: {code}  \n \n Thank you for choosing Mero Niwas. We look forward to helping you find your perfect space! \n \n Warm regards, \n The Mero Niwas Team."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

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
        
        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists. Please choose a different username.")
        
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists. Please choose a different email.")

        if UserProfile.objects.filter(contact_number=contact_number).exists():
            return HttpResponse("Contact number already exists. Please choose a different contact number.")

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

        # Generate verification code and send email
        verification_code = generate_verification_code()
        send_verification_email(email, verification_code, uname)

        # Temporarily store the user data in session
        request.session['registration_data'] = {
            'username': uname,
            'contact_number': contact_number,
            'email': email,
            'gender': gender,
            'profile_picture': profile_picture.name,
            'password':password,
            'citizenship_front': Citizen_front.name,
            'citizenship_back': Citizen_back.name,
            'accountType': accountType,
            'verification_code': verification_code,
        }

        # Redirect to verification page
        return redirect('/verify_emailbroker')

    return render(request, 'home/registerbroker.html')

def verify_emailbroker(request):
    if request.method == 'POST':
        input_code = request.POST.get("verification_code").strip()
        registration_data = request.session.get('registration_data')

        if not registration_data:
            return HttpResponse("Session expired. Please register again.")

        if input_code == registration_data['verification_code']:
            # Create the user account and save the data to the database
            user = User.objects.create_user(
                registration_data['username'],
                registration_data['email'],
                registration_data['password']
            )
            user.save()

            profile = UserProfile(
                user=user,
                contact_number=registration_data['contact_number'],
                email=registration_data['email'],
                gender=registration_data['gender'],
                profile_picture=registration_data['profile_picture'],
                Citizen_front=registration_data['citizenship_front'],
                Citizen_back=registration_data['citizenship_back'],
                accountType=registration_data['accountType']
            )
            profile.save()

            # Clear the session data
            del request.session['registration_data']

            return redirect('/LoginSuccess')
        else:
            return HttpResponse("Invalid verification code.")

    return render(request, 'home/verify_emailbroker.html')

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
        
        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists. Please choose a different username.")
        
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists. Please choose a different email.")

        if UserProfile.objects.filter(contact_number=contact_number).exists():
            return HttpResponse("Contact number already exists. Please choose a different contact number.")

        if password != confirm_password:
            return HttpResponse("Your password and confirm password must be the same.")

        if profile_picture:
            file_extension = profile_picture.name.split('.')[-1].lower()
            if file_extension not in ["jpg", "jpeg", "png", "gif"]:
                return HttpResponse("Please upload only image files (jpg, jpeg, png, gif).")

        # Generate verification code and send email
        verification_code = generate_verification_code()
        send_verification_email(email, verification_code, uname)

        # Temporarily store the user data in session
        request.session['registration_data'] = {
            'username': uname,
            'contact_number': contact_number,
            'email': email,
            'gender': gender,
            'profile_picture': profile_picture.name if profile_picture else None,
            'password':password,
            'accountType': accountType,
            'verification_code': verification_code,
        }

        # Redirect to verification page
        return redirect('/verify_emailregular')
        

    return render(request, 'home/registerregular.html')

def verify_emailregular(request):
    if request.method == 'POST':
        input_code = request.POST.get("verification_code").strip()
        registration_data = request.session.get('registration_data')

        if not registration_data:
            return HttpResponse("Session expired. Please register again.")

        if input_code == registration_data['verification_code']:
            # Create the user account and save the data to the database
            user = User.objects.create_user(
                registration_data['username'],
                registration_data['email'],
                registration_data['password']
            )
            user.save()

            profile = UserProfile(
                user=user,
                contact_number=registration_data['contact_number'],
                email=registration_data['email'],
                gender=registration_data['gender'],
                profile_picture=registration_data['profile_picture'],
                accountType=registration_data['accountType']
            )
            profile.save()

            # Clear the session data
            del request.session['registration_data']

            return redirect('/LoginSuccess')
        else:
            return HttpResponse("Invalid verification code.")

    return render(request, 'home/verify_emailregular.html')

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
