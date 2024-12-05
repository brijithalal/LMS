from django.http import HttpResponse
from django.shortcuts import render,redirect
# from onlinelibrarymanagement.library.forms import MyLoginForm
from django.shortcuts import redirect, render
from .forms import MyLoginForm, userRegistrationForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    if request.user.is_authenticated and request.session['group_name']=='admin':
        return redirect("admin_dashboard")



    else:

        return render(request,'library/base.html')



# def user_login(request):
#     if request.method == 'POST':
#         #we will be getting username and password through post
#         login_form=MyLoginForm(request.POST)
#         if login_form.is_valid():

#             cleaned_data =login_form.cleaned_data
#             auth_user = authenticate(request,username = cleaned_data['username'],password=cleaned_data['password'])
#         if auth_user is not None:
#             login(request,auth_user)
#             #get the user's group name
#             group = auth_user.groups.first()
#             group_name = group.name if group else "No group"
#             request.session['group_name'] = group_name
#             # return HttpResponse('Authenticated')
#             return redirect('home_path')
        
#         else:
#             return HttpResponse('Not Authenticated')
#     else:
#         #if error send form again
#         login_form=MyLoginForm()
#     return render(request,'library/login_form.html',
#                   {'login_form':login_form})

def user_login(request):
    if request.method == 'POST':
        # We will be getting username and password through POST
        login_form = MyLoginForm(request.POST)
        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            auth_user = authenticate(request, username=cleaned_data['username'], password=cleaned_data['password'])

            if auth_user is not None:
                login(request, auth_user)
                # Get the user's group name
                group = auth_user.groups.first()
                group_name = group.name if group else "No group"
                request.session['group_name'] = group_name

                # Check if the user is an admin and redirect accordingly
                if request.session['group_name']=='admin' :
                    # Redirect to the admin dashboard if user is an admin
                    return redirect('admin_dashboard')  # Ensure 'admin_dashboard' is correctly defined in your URLs
                elif request.session['group_name']=='user':
                    # Redirect to a regular user's home or another page
                    return redirect('home_path')  # Adjust the redirect as per your logic
                
            else:
                return HttpResponse('Not Authenticated')
    else:
        # If the form is invalid or GET request, send the form again
        login_form = MyLoginForm()
    
    return render(request, 'library/login_form.html', {'login_form': login_form})
from django.shortcuts import render
from django.http import HttpResponse

# Admin Dashboard View
def admin_dashboard(request):
    # Check if the user is authenticated and is an admin
    if request.user.is_authenticated and request.session['group_name']=='admin':
        # You can pass any necessary data to the template here
        return render(request, 'library/admin_dashboard.html')  # Render the admin dashboard template
    else:
        # If the user is not an admin, redirect them to a different page or show an error message
        return HttpResponse('You are not authorized to access this page.', status=403)




def register(request):
    if request.method =='POST':
        #we will be getting username and password through POST
        user_req_form = userRegistrationForm(request.POST)
        if user_req_form.is_valid():
            #create the form do not save it 
            new_user = user_req_form.save(commit=False)
            #set the password after validation
            #checked password == confirm password
            #password value is assigned 
            #set_password() to assign to object
            new_user.set_password(user_req_form.cleaned_data['password'])
            new_user.save() #save to db
            return redirect("home_path")
    else:
        user_req_form =userRegistrationForm()
        return render(request,'library/register_form.html',{'user_req_form':user_req_form})
    


def custom_logout(request):
    logout(request)# destroy all the session id for a particular user
    return redirect('home_path')