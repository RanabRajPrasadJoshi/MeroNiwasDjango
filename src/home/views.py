from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout ,  update_session_auth_hash
from django.http import JsonResponse
from . models import *
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def show_contactus(request):
    return render(request, 'home/ContactUs.html')

def show_successLogin(request):
    return render(request, 'home/LoginSuccess.html')

def show_aboutUs(request):
    return render(request, 'home/about_us.html')

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

@login_required
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

def show_product(request):
    rooms = Room.objects.all()

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

        if user_profile.accountType == "broker":
            return show_productBroker(request, rooms)
        else:
            return render(request, 'home/Product.html', {'rooms': rooms})

    return render(request, 'home/Product.html', {'rooms': rooms})

def show_productBroker(request, rooms):
    return render(request, 'home/ProductBroker.html', {'rooms': rooms})

def show_AddProduct(request):
    if request.method == 'POST':
        title = request.POST.get("title").strip()
        price = request.POST.get("price").strip()
        location = request.POST.get("location").strip()
        description = request.POST.get("description").strip()
        img = request.FILES.get('room-picture')
        user = request.user.username
        user_profile = UserProfile.objects.get(user=user) 
        contact_number = user_profile.contact_number
        email = user_profile.email

        if not title or not price or not location or not description:
            return HttpResponse("Please fill in all fields. Some fields are empty or only contain spaces.")
        
        if img:
            file_extension = img.name.split('.')[-1].lower()
            if file_extension not in ["jpg", "jpeg", "png", "gif"]:
                return HttpResponse("Please upload only image files (jpg, jpeg, png, gif).")
            
        room = Room.objects.create(\
            user=user,
            title=title,
            price=price,
            location=location,
            description=description,
            img=img,
            email=email,
            contact_number=contact_number
        )
        room.save()
        messages.add_message(request, messages.SUCCESS, 'Room Added successfully')
        return redirect('MyProduct')
    

    return render(request, 'home/AddProduct.html')

def show_MyProduct(request):
    if request.user.is_authenticated:
        rooms = Room.objects.filter(user=request.user.username)  # Filter rooms by the logged-in user's username
    else:
        rooms = []

    return render(request, 'home/MyProduct.html', {'rooms': rooms})

def show_updateProduct(request, room_id):
    instance = get_object_or_404(Room, id=room_id)
    
    if request.method == "POST":
        title = request.POST.get("title").strip()
        price = request.POST.get("price").strip()
        location = request.POST.get("location").strip()
        description = request.POST.get("description").strip()
        img = request.FILES.get('room-picture')

        if True:
            instance.title = title
            instance.price = price
            instance.location = location
            instance.description = description

            if img:
                file_extension = img.name.split('.')[-1].lower()
                if file_extension in ["jpg", "jpeg", "png", "gif"]:
                    instance.room_picture = img
                else:
                    messages.add_message(request, messages.ERROR, "Please upload only image files (jpg, jpeg, png, gif).")
                    return render(request, 'home/Updateproduct.html', {'room': instance})

            instance.save()
            messages.add_message(request, messages.SUCCESS, 'Room updated successfully')
            return redirect('MyProduct')  # Redirect to the 'show_my_product' view
    
    return render(request, 'home/UpdateProduct.html', {'room': instance})

def show_deleteProduct(request, room_id):
      instance = Room.objects.get(id=room_id)
      instance.delete()
      messages.add_message(request, messages.SUCCESS, "Product Deleted successfully")
      return redirect('MyProduct')

def product_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'home/room_detail.html', {'room': room})

@login_required
def show_profile(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

        context = {
            'user_profile': user_profile,
        }

        return render(request, 'home/Profile.html', context)
    
    return render(request, 'home/Profile.html', {})

@login_required
def update_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    print(user.username)
    
    if request.method == 'POST':
        # Get POST data
        username = request.POST.get('username')
        contactnumber = request.POST.get('contactnumber')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        profile_picture = request.FILES.get('profile-picture')
        Citizen_front = request.FILES.get('Citizen_front')
        Citizen_back = request.FILES.get('Citizen_back')

        # Update User model fields
        user.username = username
        user.email = email

        # Update UserProfile model fields

        user_profile.user = username
        user_profile.contact_number = contactnumber
        user_profile.email = email
        user_profile.gender = gender
        if profile_picture:
            user_profile.profile_picture = profile_picture
        if Citizen_front and user_profile.accountType == 'broker':
            user_profile.Citizen_front = Citizen_front
        if Citizen_back and user_profile.accountType == 'broker':
            user_profile.Citizen_back = Citizen_back

        # Save both models
        user.save()
        user_profile.save()

        return redirect('profile')  # Redirect to a success page or profile view
    else:
        context = {
            'user_profile': user_profile,
        }
        return render(request, 'home/updateprofile.html', context)
    
@login_required
def PasswordReset(request):
    if request.method == 'POST':
        # Get POST data
        currentPassword = request.POST.get('oldpassword')
        newPassword = request.POST.get('newpassword')
        confirmNewPassword = request.POST.get('Conformnewpassword')

        user = request.user

        if newPassword != confirmNewPassword:
            return HttpResponse("New Password and Confirm New Password must be the same")

        if not user.check_password(currentPassword):
            return HttpResponse("Current password is incorrect")

        # Set the new password
        user.set_password(newPassword)
        user.save()

        # Update session to prevent logout
        update_session_auth_hash(request, user)

        return HttpResponse("Password successfully updated")

    return render(request, 'home/PasswordReset.html')

def send_verification_password(email, code , username):
    subject = "Welcome to Mero Niwas - Verify Your Email"
    message = f"Is you username {username}, Then Your Password reset code is {code}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def show_ForgetPassword(request):
    if request.method == 'POST':
        # Get POST data
        email = request.POST.get('email')
        print(email)
        if not email:
            return HttpResponse("Please fill in all fields. Some fields are empty or only contain spaces.")
        try:
            user_profile = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return HttpResponse("No user with this email address exists.")
        
        verification_code = generate_verification_code()
        send_verification_password(email, verification_code, user_profile.user)

        # Temporarily store the user data in session
        request.session['registration_data'] = {
            'email': email,
            'verification_code': verification_code,
        }

        # Redirect to verification page
        return redirect('/VerifyPassword')
        
    return render(request, 'home/ForgetPassword.html')


def VerifyPassword(request):
    if request.method == 'POST':
        input_code = request.POST.get("verification_code").strip()
        registration_data = request.session.get('registration_data')

        if not registration_data:
            return HttpResponse("Session expired. Please register again.")

        if input_code == registration_data['verification_code']:
            return redirect('/ChangePassword')
        else:
            return HttpResponse("Invalid verification code.")

    return render(request, 'home/VerifyPassword.html')

def ChangePassword(request):
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('Conformnewpassword')
        registration_data = request.session.get('registration_data')

        if not registration_data:
            return HttpResponse("Session expired. Please try again.")

        if new_password != confirm_password:
            return HttpResponse("Passwords do not match.")

        try:
            # Retrieve user by email (assuming email is stored in registration_data)
            user = User.objects.get(email=registration_data['email'])

            # Print debug information
            print("Changing password for user:", user.username)
            print("New Password:", new_password)

            # Set new password and save user
            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            # Optionally print the updated password (hashed) for verification
            print("Updated Password (hashed):", user.password)

            return HttpResponse("Password changed successfully. You can now log in.")
        
        except User.DoesNotExist:
            return HttpResponse("User not found.")
        
        except Exception as e:
            # Print or log any other exceptions that may occur
            print("Error:", e)
            return HttpResponse("An error occurred while changing the password.")

    return render(request, 'home/PasswordForget.html')