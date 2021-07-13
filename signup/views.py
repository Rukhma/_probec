from django.shortcuts import render, redirect

from signup.models import Userreg
from django.contrib import messages
from probec_main import views


def signin(request):
    if request.method == 'POST':
        try:
            userDetails=Userreg.objects.get(email=request.POST['email'], password=request.POST['password'])
            request.session['username']=userDetails.username
            return render(request, 'dashboard.html')

        except Userreg.DoesNotExist as e:
            messages.warning(request,"Invalid credentials")
            return render(request, 'signin.html')
    else:
        if request.session.has_key('username'):
            del request.session['username']
        return render(request, 'signin.html')
    
def register(request):
    if request.method == 'POST':
         #fetching data entered into textboxes
        if request.POST.get('username') and request.POST.get('email') and request.POST.get('password'):
            if request.POST.get('password') == request.POST.get('confirm_passowrd'):
                saverecord=Userreg()
                saverecord.username=request.POST['username']
                saverecord.email=request.POST['email']
                saverecord.password=request.POST['password']
                if Userreg.objects.filter(username=saverecord.username).exists():
                    messages.warning(request,"This username already exists!")
                    return render(request, 'signup.html')
                elif Userreg.objects.filter(email=saverecord.email).exists():
                    messages.warning(request,"This email already exists!")
                    return render(request, 'signup.html')
                else:
                    saverecord.save() 
                    messages.success(request,request.POST['username'] + " is registered at Probec successfully!")
                    return render(request, 'signup.html')  
            else: 
                messages.warning(request,"Password do not match!")
                return render(request, 'signup.html')
        else:
            messages.warning(request,"SORRY")
            return render(request, 'signup.html')
    else:
        #return HttpResponse(BASE_DIR)
        return render(request, 'signup.html')




