from django.http import HttpResponse
from django.shortcuts import render
# from onlinelibrarymanagement.library.forms import MyLoginForm
from django.shortcuts import redirect, render
from .forms import MyLoginForm
from django.contrib.auth import authenticate,login

# Create your views here.
def home(request):
    return render(request,'library/base.html')



def user_login(request):
    if request.method == 'POST':
        #we will be getting username and password through post
        login_form=MyLoginForm(request.POST)
        if login_form.is_valid():

            cleaned_data =login_form.cleaned_data
            auth_user = authenticate(request,username = cleaned_data['username'],password=cleaned_data['password'])
        if auth_user is not None:
            login(request,auth_user)
            #get the user's group name
            group = auth_user.groups.first()
            group_name = group.name if group else "No group"
            request.session['group_name'] = group_name
            # return HttpResponse('Authenticated')
            return redirect('home_path')
        
        else:
            return HttpResponse('Not Authenticated')
    else:
        #if error send form again
        login_form=MyLoginForm()
    return render(request,'library/login_form.html',
                  {'login_form':login_form})
