from django.db.models.fields import EmailField
from django.shortcuts import render, redirect
from twilio.rest import Client
import random
from .models import User
from django.contrib import messages
from django.contrib.auth.models import auth


def otpverify(number = 999999, contact_number = 0):
    account_sid = 'AC3e4a64a02e49e0799b514a1e05c6efd8'
    auth_token = '###'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=f'Your OTP for registration is {number}',
            from_='+12568011009',
            to=f'+91{contact_number}'
        )
    print(message.sid)

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        print(username, email, phone, password1, password2)
        if password1 != password2 or User.objects.filter(username = username).exists():
            messages.info(request, "Password Mismatch or Username already exists")
            return redirect('/')
        else:
            otp = random.randint(100000, 999999)
            request.session['OTP'] = otp
            request.session['email'] = email
            request.session['username'] = username
            request.session['phone'] = phone
            request.session['password'] = password1
            request.session['type'] = 'registration'
            otpverify(otp, phone)
            return redirect('otp')
    else:
        return render(request, 'otpverify/register.html')

def login(request):
    if request.method == 'POST':
        user_email = request.POST['user_email']
        password = request.POST['password']
        user = User.objects.get(email = user_email)
        user = auth.authenticate(username = user.username, password = password)
        if not user:
            messages.info(request, "Invalid Email/Password")
            return redirect('login')
        else:
            user = User.objects.get(email = user_email)
            request.session['username'] = user.username
            request.session['password'] = password
            request.session['type'] = 'login'
            user = User.objects.get(email = user_email)
            login_otp = random.randint(100000, 999999)
            request.session['otp_login'] = login_otp
            otpverify(login_otp, user.phone)
            return redirect('otp')
    else:
        return render(request, 'otpverify/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def home(request):
    return render(request, 'otpverify/home.html')

def otp(request):
    if request.method == 'POST':
        if request.session['type'] == 'login':
            username = request.session['username']
            password = request.session['password']
            otp = request.POST['otp']
            if otp == str(request.session['otp_login']):
                user = auth.authenticate(username = username, password = password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('/')
                else:
                    messages.info(request, "Invalid OTP")
                    request.session.flush()
                    return redirect('login')
        else:
            otp = request.POST['otp']
            if otp == str(request.session['OTP']):
                user = User.objects.create_user(username = request.session['username'], phone = request.session['phone'], email = request.session['email'], password = request.session['password'])
                user.save()
                request.session.flush()
                return redirect('login')
    return render(request, 'otpverify/otp.html')