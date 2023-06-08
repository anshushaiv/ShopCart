
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.core.mail import EmailMessage,send_mail
from django.conf import settings
from django.views.generic import View
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.contrib.auth import authenticate,login,logout


# Create your views here.

def signup(request):
    if request.method== "POST":
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password != confirm_password:
            messages.warning(request,"Password not matching")
            return render(request,'authentication/signup.html')
        try:
            if User.objects.get(username=email):
                # return HttpResponse('Email already exists')
                messages.info(request,"email is already taken")
                return render(request, 'authentication/signup.html')
        except Exception as identifier:
            pass
        user=User.objects.create_user(email,email,password)
        user.is_active=False
        user.save()
        email_subject="Activate Your Account"
        message=render_to_string('authentication/activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        email_massage=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        print(email)
        # send_mail( email_subject,message,settings.EMAIL_HOST_USER,[email],fail_silently=True, )

        email_massage.send()
        messages.success(request, "Activate your Account by clicking the link in your mail")
        return redirect('/auths/login/')      
    return render(request, 'authentication/signup.html')

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account Activated successful")
            return redirect('/auths/login')
        return render(request,'authentication/activatefail.html')


def handlelogin(request):
    if request.method=="POST":
        user=request.POST["email"]
        pass1=request.POST["pass1"]
        auth=authenticate(username=user,password=pass1)

        if auth is not None:
            login(request,auth)
            messages.success(request,"login sucessful")
            return redirect('/')
       
        else:
            print("Not authenticated11111111111")
            messages.error(request,"Invalid credentials")
            return redirect('/auths/login')
    print("Not authenticated222222") 
    return render(request, 'authentication/login.html')

def handlelogout(request):
    logout(request)
    messages.info(request,"Log out successfully")
    return redirect('/auths/login')