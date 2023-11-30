from django.shortcuts import render,redirect
from  passlib.hash import pbkdf2_sha256
from  login.models import bloguser
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
import math, random


def generateOTP() :
    digits = "0123456789"
    create_OTP = ""

    for i in range(6) :
       create_OTP += digits[math.floor(random.random() * 10)]
 
    return create_OTP

def validate_password(password: str):
    if len(password)>=8:
        lower = 0
        upper = 0
        special = 0
        number = 0
        for i in password:
            if i.islower():
                lower += 1
            
            elif i.isupper():
                upper += 1

            elif i.isnumeric():
                number += 1

            elif i in "~!@#$%^&*()_[]()":
                special += 1

        if lower>=1 and upper>=1 and number>=1 and special>=1:
                return True
    return False


# login blog user
def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            bloguser.objects.get(email=email)
        except:
             msg="User does not exiat"
             return render(request,"login.html",{"msg":msg})
            
        else:
            obj=bloguser.objects.get(email=email)
            name=obj.name
            getpass=obj.password

            decode_pass=pbkdf2_sha256.verify(password,getpass)

            if obj.email==email and decode_pass == True:
                    request.session["email"]=email
                   # request.session["islogin"]="true"
                    context= {'data':name}
                    return render(request,"result.html",context)
            else:
                    msg="Invalid password"
                    return render(request,"login.html",{"msg":msg})

    return render(request,"login.html")


# Register bog user
def register(request):
    if request.method=='POST': 
        name=request.POST.get('name')   
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        enc_pass = pbkdf2_sha256.hash(password)
      
        try:
            bloguser.objects.get(email=email)
            
        except:
            if validate_password(password):
              
                OTP=generateOTP()

                request.session['otp']=OTP
                request.session['name']=name
                request.session['email']=email
                request.session['phone']=phone
                request.session['password']=enc_pass


                subject = 'OTP form blogger'
                message = f' OPT is :{OTP}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail( subject, message, email_from, recipient_list )
                return redirect("/login/registerotp/")
                #return render(request,"register_result.html",context)
            else:
                msg="Invalid password. Please follow password condition"
                render(request,"register.html",{'msg':msg})

           
        else:
            context={'data':"User already register"}
            return render(request,"register_result.html",context)

    return render(request,"register.html")

def registerotp(request):
    if request.method == "POST":
        otp=request.POST.get('otp')
        otp_session=request.session["otp"]
        if otp == otp_session:   
            name=request.session['name']
            email=request.session['email']
            phone=request.session['phone']
            enc_pass=request.session['password']

            user_data=bloguser(name=name,email=email,phone=phone,password=enc_pass)
            user_data.save()
            context={'data':name}
            return render(request,"register_result.html",context)
        else:
            msg="Incorrect OTP"
            return render(request,"register.html",{"msg":msg})
    
    if request.method=="GET":
        return render(request,"otp.html")
    

def update(request):
    if request.method=='POST':
       
        email=request.POST.get('email')
        oldpassword=request.POST.get('oldpassword')
        newpassword=request.POST.get('newpassword')

        
        newpass_encode= pbkdf2_sha256.hash(newpassword)
        request.session['email']=email
        request.session['newpassword']=newpass_encode

        try:
            bloguser.objects.get(email=email)
        except:
             return HttpResponse("User does not exists. ")
            
        else: 
            obj=bloguser.objects.get(email=email)

            OTP=generateOTP()
            request.session['otp']=OTP
            subject = 'OTP for password change'
            message = f'Hi,{obj.name} \n OPT is :{OTP}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list )
           
            return redirect("/login/updateotp/")
           # return render(request,"otp.html")

    return render(request,"updatepassword.html")

def updateotp(request):
    if request.method == "POST":
        otp=request.POST.get('otp')
        otp_session=request.session["otp"]
        email=request.session["email"]
        if otp==otp_session:
            obj=bloguser.objects.get(email=email)
            newpass_encode=request.session['newpassword']
            obj.password=newpass_encode
            obj.save()
            return  render(request,"otp_result.html")
        else:
            msg="Incorrect OTP"
            return render(request,"otp.html",{"msg":msg})
    
    if request.method=="GET":
        return render(request,"otp.html")
    
def logout(request):
    try:
        del request.session['email']
        del  request.session['name']
        del request.session['phone']
        del request.session['password']
    except KeyError:
       pass
    return redirect('/login/')

def loginresult(request):
    if 'email' in request.session:
        current_user = request.session['email']
        param = {'current_user': current_user}
        return render(request, 'result.html', param)
    else:
        return redirect('login')
    