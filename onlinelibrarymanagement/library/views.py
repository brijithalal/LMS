from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
# from onlinelibrarymanagement.library.forms import MyLoginForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Authors, Book, Category, PlanCategory, Rent, SubscriptionPlans, Subscriptions,User
from .forms import AddAuthorForm, AddBookForm, AddCategoryForm, EditAuthorForm, EditBookForm, EditCategoryForm, EditSubscriptionForm, MyLoginForm,  userRegistrationForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):  
    if request.user.is_authenticated and request.session['group_name']=='admin':
        return redirect("admin_dashboard")
        
    elif request.user.is_authenticated and request.session['group_name']=='user':
        view_books = Book.objects.all()
        notifications = Notification.objects.filter(user=request.user)
        unread_count = notifications.filter(is_read=False).count()  # Assuming you have an `is_read` field

        context = {
            'notifications': notifications,
            'unread_count': unread_count,
            'view_books':view_books
        }
        print(view_books)
    else:
        view_books = Book.objects.all()
        context={
            'view_books':view_books
        }
    return render(request,'library/topbar.html',context)
    

        # return render(request,'library/base.html')


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
    
    if request.user.is_authenticated:
        return redirect('home_path')
    else:
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
                    else:
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
@login_required
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
    

@login_required
def custom_logout(request):
    logout(request)# destroy all the session id for a particular user
    return redirect('home_path')


# def add_books(request):
#     session_data = request.session.get('book_data', {})
#     if request.method == 'POST':
#         add_book = AddBookForm(request.POST,request.FILES)

#         if add_book.is_valid():

#             add_book.save()
#             request.session.pop('book_data', None)

        
#             return redirect('admin_dashboard')
#         else:
#             print(add_book.errors)
#     else:
#         #   On GET request, retrieve session data if available
#         # book_data = request.session.get('book_data', {})

#         # Initialize the form with the session data
#         # add_book = AddBookForm(initial=book_data)


#         add_book = AddBookForm(session_data=session_data)
#     return render(request,'library/add_book.html',{'add_book_form':add_book})


# def add_books(request):
#     if request.method == 'POST':
#         add_book = AddBookForm(request.POST, request.FILES)

#         if add_book.is_valid():
#             add_book.save()

#             # Clear session data after saving the book
#             request.session.pop('book_data', None)
            
#             return redirect('admin_book_list')
#         else:
#             print(add_book.errors)
#     else:
#         # On GET request, retrieve session data if available
#         book_data = request.session.get('book_data', {})
#         print(book_data)
#         # Initialize the form with the session data
#         add_book = AddBookForm(initial=book_data)
        
#     # Store the current form data in session before redirecting
#     if 'add_author' in request.GET:  # Check if "Add Author" button was clicked
#         # Save form data in session before redirecting
#         book_data = add_book.cleaned_data if add_book.is_valid() else request.POST
#         request.session['book_data'] = book_data  # Save form data in session
#         print(request.session['book_data'])
#         print("hello")
        
#         return redirect('add_author')  # Redirect to add_author page

#     if 'add_category' in request.GET:  # Check if "Add Category" button was clicked
#         # Save form data in session before redirecting
#         book_data = add_book.cleaned_data if add_book.is_valid() else request.POST
#         request.session['book_data'] = book_data  # Save form data in session
#         print("hello",request.session['book_data'])
#         return redirect('add_category')  # Redirect to add_category page

#     return render(request, 'library/add_book.html', {'add_book_form': add_book})

# def add_books(request):
#     # Initialize form with session data if it exists
#     book_data = request.session.get('book_data', {})
#     add_book = AddBookForm(initial=book_data)

#     if request.method == 'POST':
#         add_book = AddBookForm(request.POST, request.FILES)
#         if add_book.is_valid():
#             # Save the book
#             add_book.save()

#             # Clear session data after saving the book
#             if 'book_data' in request.session:
#                 del request.session['book_data']

#             return redirect('admin_dashboard')  # Redirect after saving
#         else:
#             print(add_book.errors)  # Print errors if form is invalid

#     # Handle "Add Author" button click
#     if 'add_author' in request.GET:
#         if add_book.is_valid():
#             request.session['book_data'] = add_book.cleaned_data  # Save valid form data to session
#         else:
#             request.session['book_data'] = request.POST.dict()  # Save raw POST data to session
#         return redirect('add_author')

#     # Handle "Add Category" button click
#     if 'add_category' in request.GET:
#         if add_book.is_valid():
#             request.session['book_data'] = add_book.cleaned_data  # Save valid form data to session
#         else:
#             request.session['book_data'] = request.POST.dict()  # Save raw POST data to session
#         return redirect('add_category')

#     return render(request, 'library/add_book.html', {'add_book_form': add_book})

@login_required
def add_books(request):
    # Initialize the form with session data if available
    book_data = request.session.get('book_data', {})
    add_book_form = AddBookForm(initial=book_data)

    if request.method == 'POST':
        add_book_form = AddBookForm(request.POST, request.FILES)
        if add_book_form.is_valid():
            # Save the book
            add_book_form.save()

            # Clear session data after saving the book
            if 'book_data' in request.session:
                del request.session['book_data']

            return redirect('admin_dashboard')  # Redirect after saving
        else:
            print(add_book_form.errors)

    # Save form data to session before redirecting to add author or category
    if 'add_author' in request.GET:
        if add_book_form.is_valid():
            request.session['book_data'] = add_book_form.cleaned_data
        else:
            request.session['book_data'] = request.POST.dict()
        return redirect('add_author')

    if 'add_category' in request.GET:
        if add_book_form.is_valid():
            request.session['book_data'] = add_book_form.cleaned_data
        else:
            request.session['book_data'] = request.POST.dict()
        return redirect('add_category')

    return render(request, 'library/add_book.html', {'add_book_form': add_book_form})


# def add_books(request):
#     # Handle POST request (form submission)

#     if request.method == 'POST':
#         add_book = AddBookForm(request.POST, request.FILES)

#         if add_book.is_valid():
#             # Save the book
#             new_book = add_book.save()

#             # After saving, clear session data
#             request.session.pop('book_data', None)  # Clear session data after saving

#             return redirect('admin_dashboard')  # Redirect to another page after saving the book
#         else:
#             print(add_book.errors)  # Print errors if form is invalid
#     else:
#         # Retrieve book data from session (if exists)
#         book_data = request.session.get('book_data', {})

#         # Initialize the form with the session data (if available)
#         add_book = AddBookForm(initial=book_data)

#     # Handle actions like "Add Author" and "Add Category"
#     if 'add_author' in request.GET:  # Check if "Add Author" button was clicked
#         # Store the current form data in session before redirecting
#         book_data = add_book.cleaned_data if add_book.is_valid() else request.POST
#         request.session['book_data'] = book_data  # Save form data in session

#         return redirect('add_author')  # Redirect to add_author page

#     if 'add_category' in request.GET:  # Check if "Add Category" button was clicked
#         # Store the current form data in session before redirecting
#         book_data = add_book.cleaned_data if add_book.is_valid() else request.POST
#         request.session['book_data'] = book_data  # Save form data in session

#         return redirect('add_category')  # Redirect to add_category page

#     return render(request, 'library/add_book.html', {'add_book_form': add_book})

@login_required
def edit_books(request,pk):
    if request.method == 'POST':
        book_details = get_object_or_404(Book, id=pk)
        edit_book = EditBookForm(request.POST or None,request.FILES or None,instance=book_details)

        if edit_book.is_valid():
            edit_book.save()

            return redirect('admin_dashboard')
        else:
            print(edit_book.errors)
    else:

        edit_book  = EditBookForm()
    return render(request,'library/edit_book.html',{'edit_book_form':edit_book})

def admin_book_list(request):
    book_list = Book.objects.all()
    return render(request,'library/admin_view_booklist.html',{'view_booklist':book_list})
        


@login_required
def delete_book(request,pk):
    #get the post with the id value in the table
    book_list = get_object_or_404(Book,id = pk)
    book_list.delete()
    return redirect('admin_book_list')

# def add_authors_from_book(request):
#     if request.method == 'POST':
#         add_author = AddAuthorForm(request.POST)
#         if add_author.is_valid():
#             add_author.save()
#             # Redirect back to the add book page or any desired page

#             return redirect('add_book')  # Adjust the name of the add_books URL as needed
#         else:
#             print(add_author.errors)
#     else:
#         add_author = AddAuthorForm()
#     return render(request, 'library/add_author_from_addbookform.html', {'add_author_form': add_author})


# def add_authors_from_book(request):
#     if request.method == 'POST':
#             add_author = AddAuthorForm(request.POST)
#             if add_author.is_valid():
#                 # Save the author
#                 add_author.save()

#                 # After saving the author, store the current book data in session
#                 # Retrieve the existing book data from session
#                 book_data = request.session.get('book_data', {})
#                 book_data['author'] = add_author.cleaned_data['author_name']  # Assuming 'name' is the field name in AddAuthorForm

#                 # Store the updated book data back to session
#                 request.session['book_data'] = book_data

#                 # Redirect back to the Add Book form
#                 return redirect('add_book')
#     else:
#         add_author = AddAuthorForm()

#     return render(request, 'library/add_author_from_addbookform.html', {'add_author_form': add_author})


@login_required
def add_authors_from_book(request):
    if request.method == 'POST':
        add_author = AddAuthorForm(request.POST)
        if add_author.is_valid():
            # Save the author
            add_author.save()

            # Get existing book data from session and save the new author
            book_data = request.session.get('book_data', {})
            book_data['author'] = add_author.cleaned_data['author_name']  # Assuming 'name' is the field name in AddAuthorForm

            # Store updated book data back in session
            request.session['book_data'] = book_data

            # Redirect back to Add Book form
            return redirect('add_book')
    else:
        add_author = AddAuthorForm()

    return render(request, 'library/add_author_from_addbookform.html', {'add_author_form': add_author})


@login_required
def add_authors_admin(request):
    if request.method == 'POST':
        add_author_admin = AddAuthorForm(request.POST)
        if add_author_admin.is_valid():
            add_author_admin.save()
            # Redirect back to the add book page or any desired page

            return redirect('view_author')  # Adjust the name of the add_books URL as needed
        else:
            print(add_author_admin.errors)
    else:
        add_author_admin = AddAuthorForm()
    return render(request, 'library/add_author_from_admin.html', {'add_author_form_admin': add_author_admin})


@login_required
def add_categories_from_book(request):
    if request.method == 'POST':
        add_category = AddCategoryForm(request.POST)
        if add_category.is_valid():
            add_category.save()
            # Redirect back to the add book page or any desired page
            return redirect('add_book')  # Adjust the name of the add_books URL as needed
        else:
            print(add_category.errors)
    else:
        add_category = AddCategoryForm()
    return render(request, 'library/add_category_from_book.html', {'add_category_form': add_category})


@login_required
def add_categories_from_admin(request):
    if request.method == 'POST':
        add_category_admin = AddCategoryForm(request.POST)
        if add_category_admin.is_valid():
            add_category_admin.save()
            # Redirect back to the add book page or any desired page
            return redirect('view_category')  # Adjust the name of the add_books URL as needed
        else:
            print(add_category_admin.errors)
    else:
        add_category_admin = AddCategoryForm()
    return render(request, 'library/add_category_from_admin.html', {'add_category_admin': add_category_admin})


@login_required
def view_author(request):
    author_list = Authors.objects.all()
    return render(request,'library/admin_view_authors.html',{'author_list':author_list})
    
@login_required
def edit_author(request,pk):
    if request.method == 'POST':
        author_details = get_object_or_404(Authors, id=pk)
        edit_author = EditAuthorForm(request.POST or None,request.FILES or None,instance=author_details)

        if edit_author.is_valid():
            edit_author.save()

            return redirect('view_author')
        else:
            print(edit_author.errors)
    else:

        edit_author  = EditAuthorForm()
    return render(request,'library/edit_authors.html',{'edit_author_form':edit_author})


@login_required
def delete_authors(request,pk):
    #get the post with the id value in the table
    delete_list = get_object_or_404(Authors,id = pk)
    delete_list.delete()
    return redirect('view_author')

# def admin_book_list(request):
#     book_list = Book.objects.all()
#     return render(request,'library/admin_view_booklist.html',{'view_booklist':book_list})


@login_required
def admin_book_list(request):
    search_query = request.GET.get('search', '')  # Get the search term from the GET request

    
    if search_query:
        # Filter books where the title or author matches the search query
        books = Book.objects.filter(Q(book_title__icontains=search_query) | Q(author__author_name__icontains=search_query))
    else:
        # If no search query, display all books
        books = Book.objects.all()
    
    context = {
        'view_booklist': books,
        'search_query': search_query,  # Pass the search query back to the template for the search bar
    }
    return render(request, 'library/admin_view_booklist.html', context)

@login_required
def view_book_details(request,pk):
    book_list = get_object_or_404(Book, pk=pk)
    return render(request,'library/admin_book_view.html',{'book_list':book_list})

@login_required
def view_category(request):
    category_list = Category.objects.all()
    return render(request,'library/admin_view_category.html',{'category_list':category_list})


@login_required
def edit_category(request,pk):
    category_details = get_object_or_404(Category, id=pk)
    # plan_details = get_object_or_404(PlanCategory,id = pk)

    if request.method == 'POST':
        edit_category = EditCategoryForm(request.POST or None,request.FILES or None,instance=category_details)

        if edit_category.is_valid():
            edit_category.save()

            return redirect('view_category')
        else:
            print(edit_category.errors)
    else:

        edit_category  = EditCategoryForm(instance=category_details)
    return render(request,'library/edit_category.html',{'edit_category_form':edit_category})


@login_required
def delete_category(request,pk):
    #get the post with the id value in the table
    delete_list = get_object_or_404(Category,id = pk)
    delete_list.delete()
    return redirect('view_category')



def book_list(request):
    # Get the search query from the GET request
    search_query = request.GET.get('search', '')

    # Filter the books by title or author based on the search query
    if search_query:
        books = Book.objects.filter(
            Q(book_title__icontains=search_query) | Q(author__icontains=search_query)
        )
    else:
        books = Book.objects.all()  # If no search, show all books

    context = {
        'view_booklist': books,
        'search_query': search_query,
    }
    return render(request, 'library/admin_view_booklist.html', context)

@login_required
def author_list(request):
    search_query = request.GET.get('search', '')  # Get the search term from the request
    if search_query:
        authors = Authors.objects.filter(author_name__icontains=search_query)  # Filter authors by name
    else:
        authors = Authors.objects.all()  # Show all authors if no search query

    context = {
        'author_list': authors,
        'search_query': search_query,
    }
    return render(request, 'library/admin_view_authors.html', context)


@login_required
def category_list(request):
    search_query = request.GET.get('search', '')  # Capture the search term
    if search_query:
        categories = Category.objects.prefetch_related('plans__plan').filter(category_name__icontains=search_query)  # Case-insensitive search with related plans
    else:
        categories = Category.objects.prefetch_related('plans__plan').all()  # Fetch all categories with related plans

    context = {
        'category_list': categories,
        'search_query': search_query,
    }
    return render(request, 'library/admin_view_category.html', context)


@login_required
def view_subscriptions(request):
    subscriptions_list = SubscriptionPlans.objects.all()
    print(subscriptions_list)
    return render(request,'library/view_subscriptions.html',{'subscriptions_list':subscriptions_list})


# def view_subscriptions_plan_user(request):
#     # subscriptions_list = SubscriptionPlans.objects.all()
#     # categories = Category.objects.prefetch_related('plans__plan').all()
#     subscriptions_list = SubscriptionPlans.objects.prefetch_related('plans__category').all()
#     print(subscriptions_list)
#     return render(request,'library/view_subscriptions_plans_user.html',{'subscriptions_list':subscriptions_list})


def view_all_books_home(request):
    view_books = Book.objects.all()
    print(view_books)
    return render(request,'library/topbar.html',{"view_books":view_books})


# def rent_book(request, book_id):
#     # Assuming you have access to the current logged-in user
#     user = request.user
#     book = Book.objects.get(id=book_id)
    
#     # Get the user's subscription plan
#     subscription = Subscriptions.objects.get(user=user)
#     plan = subscription.plan  # This gives you the SubscriptionPlans object
    
#     # Set rental duration based on the subscription plan
#     if plan.plan_name == "Gold":
#         rental_duration = timedelta(days=28)  # 28 days for Gold Plan
#     elif plan.plan_name == "Platinum":
#         rental_duration = timedelta(days=60)  # 2 months for Platinum Plan
#     elif plan.plan_name == "Diamond":
#         rental_duration = timedelta(days=90)  # 3 months for Diamond Plan
#     else:
#         rental_duration = timedelta(days=28)  # Default to 28 days if plan is not recognized

#     # Now, create a rental record (you can modify this to your exact requirement)
#     rental_end_date = timezone.now() + rental_duration

#     # Assuming you have a model to track rentals
#     rental = Rent.objects.create(
#         user=user,
#         book=book,
#         rental_start_date=timezone.now(),
#         rental_end_date=rental_end_date
#     )

#     return redirect('rental_success')


# @login_required
# def rent_book(request, book_id):
#     # Assuming you have access to the current logged-in user
#     user = request.user
#     try:
#         book = Book.objects.get(id=book_id)
#     except Book.DoesNotExist:
#         # messages.error(request, "The book you are trying to rent does not exist.")
#         return redirect('home_path')

#     try:
#         # Get the user's active subscription plan
#         #gte is greater than or equal to
#         subscription = Subscriptions.objects.filter(user=user, end_date__gte=timezone.now()).first() 
#         if not subscription:
#             messages.info(request, "You are not subscribed to any active plan. Please subscribe to a plan to rent books.")
#             return redirect('view_subscriptions_plans_user')  

#         plan = subscription.plan  # This gives you the SubscriptionPlans object
#     except Subscriptions.DoesNotExist:
#         # If the user is not subscribed to any plan
#         messages.info(request, "You are not subscribed to any plan. Please subscribe to a plan to rent books.")
#         return redirect('view_subscriptions_plans_user')  

#     # Check if the user's subscription plan allows access to the book's category
#     allowed_categories = PlanCategory.objects.filter(plan=plan).values_list('category', flat=True)
#     if book.category.id not in allowed_categories:
#         messages.info(request, "Your subscription plan does not give you access to this book's category. Please subscribe to a higher plan.")
#         return redirect('view_subscriptions_plans_user')  

#     # Set rental duration based on the subscription plan
#     if plan.plan_name == "Gold":
#         rental_duration = timedelta(days=28)  
#     elif plan.plan_name == "Platinum":
#         rental_duration = timedelta(days=60) 
#     elif plan.plan_name == "Diamond":
#         rental_duration = timedelta(days=100)  
#     else:
#         rental_duration = timedelta(days=28)  # Default to 28 days if plan is not recognized

#     # Show confirmation to the user about renting the book
#     if request.method == 'POST':
      
#         rental_end_date = timezone.now() + rental_duration
#         rental = Rent.objects.create(
#             user=user,
#             book=book,
#             rent_date=timezone.now(),
#             expiry_date=rental_end_date
#         )
#         messages.success(request, f"You have rented '{book.book_title}' for {rental_duration.days} days. Rental ID: {rental.id}")
#         return redirect('rental_success')  # Redirect to a success page or book details

#     # If it's not a POST request, show the confirmation page
#     return render(request, 'library/rent_confirmation.html', {
#         'book': book,
#         'rental_duration': rental_duration,
#         'plan': plan
#     })

# @login_required
# def rent_book(request, book_id):
#     # Assuming you have access to the current logged-in user
#     user = request.user
#     try:
#         book = Book.objects.get(id=book_id)
#     except Book.DoesNotExist:
#         return redirect('home_path')

#     try:
#         # Get the user's active subscription plan
#         subscription = Subscriptions.objects.filter(user=user, end_date__gte=timezone.now()).first()
#         if not subscription:
#             messages.info(request, "You are not subscribed to any active plan. Please subscribe to a plan to rent books.")
#             return redirect('view_subscriptions_plans_user')

#         plan = subscription.plan  # This gives you the SubscriptionPlans object
#     except Subscriptions.DoesNotExist:
#         messages.info(request, "You are not subscribed to any plan. Please subscribe to a plan to rent books.")
#         return redirect('view_subscriptions_plans_user')

#     # Check if the user's subscription plan allows access to the book's category
#     allowed_categories = PlanCategory.objects.filter(plan=plan).values_list('category', flat=True)
#     if book.category.id not in allowed_categories:
#         messages.info(request, "Your subscription plan does not give you access to this book's category. Please subscribe to a higher plan.")
#         return redirect('view_subscriptions_plans_user')

#     # Set rental duration based on the subscription plan
#     if plan.plan_name == "Gold":
#         rental_duration = timedelta(days=28)
#     elif plan.plan_name == "Platinum":
#         rental_duration = timedelta(days=60)
#     elif plan.plan_name == "Diamond":
#         rental_duration = timedelta(days=100)
#     else:
#         rental_duration = timedelta(days=28)  # Default to 28 days if plan is not recognized

#     # Handle payment form submission
#     if request.method == 'POST':
#         payment_type = request.POST.get('payment_type')  # Retrieve selected payment type

#         if not payment_type:
#             # Return an error if no payment type is selected
#             messages.error(request, "Please select a payment method.")
#             return render(request, 'library/rent_confirmation.html', {'book': book, 'rental_duration': rental_duration, 'plan': plan})

#         # Decrease the stock of the book (if needed)
#         book.stock_quantity -= 1
#         book.save()

#         # Create a rental record
#         rental_end_date = timezone.now() + rental_duration
#         rental = Rent.objects.create(
#             user=user,
#             book=book,
#             rent_date=timezone.now(),
#             expiry_date=rental_end_date
#         )

#         # Create a payment record for the rental
#         payment = Payment.objects.create(
#                 amount=book.price,
#                 payment_type=payment_type,  # Save the selected payment type
#                 user=request.user,
#                 payment_action=3  # Indicating a purchase action
#             )

#         # Success message and redirect
#         messages.success(request, f"You have rented '{book.book_title}' for {rental_duration.days} days. Rental ID: {rental.id}. Payment ID: {payment.id}")
#         return redirect('rental_success')  # Redirect to a success page or book details

#     # If it's not a POST request, show the confirmation page
#     return render(request, 'library/rent_confirmation.html', {
#         'book': book,
#         'rental_duration': rental_duration,
#         'plan': plan
#     })

@login_required
def rent_book(request, book_id):
    # Assuming you have access to the current logged-in user
    user = request.user
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return redirect('home_path')

    try:
        # Get the user's active subscription plan
        subscription = Subscriptions.objects.filter(user=user, end_date__gte=timezone.now()).first()
        if not subscription:
            messages.info(request, "You are not subscribed to any active plan. Please subscribe to a plan to rent books.")
            return redirect('view_subscriptions_plans_user')

        plan = subscription.plan  # This gives you the SubscriptionPlans object
    except Subscriptions.DoesNotExist:
        messages.info(request, "You are not subscribed to any plan. Please subscribe to a plan to rent books.")
        return redirect('view_subscriptions_plans_user')

    # Check if the user's subscription plan allows access to the book's category
    allowed_categories = PlanCategory.objects.filter(plan=plan).values_list('category', flat=True)
    if book.category.id not in allowed_categories:
        messages.info(request, "Your subscription plan does not give you access to this book's category. Please subscribe to a higher plan.")
        return redirect('view_subscriptions_plans_user')
    
        # Check if the user has already rented this book
    existing_rental = Rent.objects.filter(user=user, book=book, expiry_date__gte=timezone.now()).first()
    if existing_rental:
        messages.info(request, "You have already rented this book.")
        return redirect('home_path')  # Or redirect to another page where the user can view their rented books


    # Set rental duration based on the subscription plan
    if plan.plan_name == "Gold":
        rental_duration = timedelta(days=28)
    elif plan.plan_name == "Platinum":
        rental_duration = timedelta(days=60)
    elif plan.plan_name == "Diamond":
        rental_duration = timedelta(days=100)
    else:
        rental_duration = timedelta(days=28)  # Default to 28 days if plan is not recognized

    # Handle payment form submission
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')  # Retrieve selected payment type
        if not payment_type:
            # messages.error(request, "Please select a payment method.")
            return render(request, 'library/rent_confirmation.html', {'book': book, 'rental_duration': rental_duration, 'plan': plan})

        # Validate payment-specific fields based on selected payment type
        if payment_type == 'googlepay':
            upi_id = request.POST.get('upi_id')
            if not upi_id:
                # messages.error(request, "Please enter your UPI ID for Google Pay.")
                return render(request, 'library/rent_confirmation.html', {'book': book, 'rental_duration': rental_duration, 'plan': plan})

        elif payment_type == 'creditcard':
            card_number = request.POST.get('card_number')
            card_expiry = request.POST.get('card_expiry')
            card_cvv = request.POST.get('card_cvv')
            if not card_number or not card_expiry or not card_cvv:
                # messages.error(request, "Please fill in all the credit card details.")
                return render(request, 'library/rent_confirmation.html', {'book': book, 'rental_duration': rental_duration, 'plan': plan})

        elif payment_type == 'banktransfer':
            account_number = request.POST.get('account_number')
            ifsc_code = request.POST.get('ifsc_code')
            if not account_number or not ifsc_code:
                # messages.error(request, "Please provide both the Bank Account Number and IFSC Code.")
                return render(request, 'library/rent_confirmation.html', {'book': book, 'rental_duration': rental_duration, 'plan': plan})

        # If payment details are valid, proceed with creating the rental and payment
        # Decrease the stock of the book (if needed)
        book.stock_quantity -= 1
        book.save()

        # Create a rental record
        rental_end_date = timezone.now() + rental_duration
        rental = Rent.objects.create(
            user=user,
            book=book,
            rent_date=timezone.now(),
            expiry_date=rental_end_date
        )

        # Create a payment record for the rental
        payment = Payment.objects.create(
            amount=book.rent_price,  # Assuming you have rental_price field in the Book model
            payment_type=payment_type,  # Save the selected payment type
            user=request.user,
            payment_action=3  # Indicating a rent action
        )

        # Success message and redirect
        messages.success(request, f"You have rented '{book.book_title}' for {rental_duration.days} days. Rental ID: {rental.id}. Payment ID: {payment.id}")
        return redirect('rental_success')  # Redirect to a success page or book details

    # If it's not a POST request, show the confirmation page
    return render(request, 'library/rent_confirmation.html', {
        'book': book,
        'rental_duration': rental_duration,
        'plan': plan
    })



@login_required
def rental_success(request):
    return render(request, 'library/rental_success.html')

@login_required
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Redirect to a category list or success page
    else:
        form = AddCategoryForm()
    return render(request, 'library/add_category_from_admin.html', {'form': form})


@login_required
def edit_subscriptions(request, pk):
    subscription_plan = get_object_or_404(SubscriptionPlans, id=pk)

    if request.method == 'POST':
        form = EditSubscriptionForm(request.POST, instance=subscription_plan)
        if form.is_valid():
            form.save()
            return redirect('view_subscriptions')  # Replace with the actual redirect URL
        else:
            print(form.errors)
    else:
        # Pre-select existing categories for the plan
        existing_categories = PlanCategory.objects.filter(plan=subscription_plan).values_list('category', flat=True)
        form = EditSubscriptionForm(instance=subscription_plan, initial={'categories': existing_categories})

    return render(request, 'library/edit_subscriptions.html', {'form': form})



# def user_subscription_plan(request,pk):
#     plan=get_object_or_404(request.GET,id=pk)
    


# def membership_and_rentals_view(request):
#     plans = SubscriptionPlans.objects.prefetch_related('plans__category').all()
#     return render(request, 'library/view_subscriptions_plans_user.html', {'plans': plans})



# def subscription_details(request, plan_id):
#     selected_plan = get_object_or_404(SubscriptionPlans, id=plan_id)
#     return render(request, 'subscription_details.html', {'plan': selected_plan})


# def plan_details(request, plan_id):
#     plan = get_object_or_404(SubscriptionPlans, id=plan_id)
#     plan_categories = PlanCategory.objects.filter(plan=plan)
    
#     # Fetch associated categories for this plan
#     categories = [plan_category.category.category_name for plan_category in plan_categories]
    
#     return render(request, 'plan_details.html', {
#         'plan': plan,
#         'categories': categories
#     })


# def subscribe(request, plan_id):
#     plan = SubscriptionPlans.objects.get(id=plan_id)
    
#     # Check if the user is already subscribed to any plan
#     user_subscription = Subscriptions.objects.filter(user=request.user, end_date__gte=datetime.now()).first()

#     if user_subscription:
#         # If the user is already subscribed to a plan, check if it's a higher plan
#         if user_subscription.plan.price < plan.price:
#             # If the new plan is higher, prompt to upgrade
#             return render(request, 'upgrade_prompt.html', {
#                 'current_plan': user_subscription.plan,
#                 'new_plan': plan
#             })
#         else:
#             # If they are already on a plan that is equal or higher
#             return render(request, 'already_subscribed.html')
    
#     # If the user is not subscribed to any plan, show the subscription details page
#     return render(request, 'plan_details.html', {
#         'plan': plan
#     })




# def plan_details(request, plan_id):
#     plan = get_object_or_404(SubscriptionPlans, id=plan_id)
#     return render(request, 'library/view_subscriptions_plans_user.html', {
#         'plan': plan
#     })



# @login_required
# def confirm_subscription(request, plan_id):
#     plan = SubscriptionPlans.objects.get(id=plan_id)

#     # Calculate the subscription start and end dates
#     start_date = timezone.now()
#     end_date = start_date + timedelta(days=plan.duration)

#     # Create a new subscription record
#     subscription = Subscriptions.objects.create(
#         user=request.user,
#         plan=plan,
#         start_date=start_date,
#         end_date=end_date
#     )

#     # Redirect to a confirmation page
#     return redirect('subscription_success')




# def subscription_plans_view(request):
#     # Retrieve all subscription plans
#     plans = SubscriptionPlans.objects.all()
#     plans_with_categories = []

#     # Retrieve associated categories for each plan
#     for plan in plans:
#         categories = PlanCategory.objects.filter(plan=plan).select_related('category')
#         category_names = [cat.category.category_name for cat in categories]
#         plans_with_categories.append({
#             'plan_name': plan.plan_name,
#             'price': plan.price,
#             'duration': plan.duration,
#             'categories': category_names
#         })

#     return render(request, 'subscriptions.html', {'plans_with_categories': plans_with_categories})




# @login_required
# def user_books_view(request):
#     # Get the user's active subscription
#     subscription = Subscriptions.objects.filter(user=request.user).first()
#     if subscription:
#         # Get categories associated with the user's subscription plan
#         categories = PlanCategory.objects.filter(plan=subscription.plan).select_related('category')
#         category_ids = [cat.category.id for cat in categories]

#         # Get books in the allowed categories
#         accessible_books = Book.objects.filter(category_id__in=category_ids)
#     else:
#         accessible_books = []

#     return render(request, 'user_books.html', {'books': accessible_books})








# def subscribe_plan(request, plan_id):
#     # Retrieve the subscription plan by ID
#     plan = get_object_or_404(SubscriptionPlans, id=plan_id)

#     # Calculate subscription start and end dates
#     start_date = now()
#     end_date = start_date + timedelta(days=plan.duration)

#     # Check if the user already has an active subscription
#     active_subscription = Subscriptions.objects.filter(user=request.user, end_date__gte=now()).first()
#     if active_subscription:
#         messages.warning(request, "You already have an active subscription. Please wait until it expires.")
#         return redirect('subscription_plans')

#     # Create a new subscription for the user
#     Subscriptions.objects.create(
#         user=request.user,
#         plan=plan,
#         start_date=start_date,
#         end_date=end_date
#     )

#     # Add a success message and redirect the user
#     messages.success(request, f"Successfully subscribed to the {plan.plan_name} plan!")
#     return redirect('user_books')


from dateutil.relativedelta import relativedelta
# @login_required
# def subscribe(request,pk):
#     user = request.user
#     plan=get_object_or_404(SubscriptionPlans,id = pk)
#     end_date = timezone.now() + relativedelta(months=plan.duration)
    
#     subscription = Subscriptions.objects.create(
#         user=user,
#         plan=plan,
#         start_date=timezone.now(),
#         end_date=end_date,
#         status=3 # Initial status set to "pending"
#     )
#     return render(request,'library/payment.html', {"subscription_id": subscription})

@login_required
def subscribe(request, pk):
    user = request.user
    plan = get_object_or_404(SubscriptionPlans, id=pk)

    # Check if the user already holds this plan
    active_subscription = Subscriptions.objects.filter(
        user=user,
        plan=plan,
        status=1  # Assuming status=1 means "active"
    ).first()

    if active_subscription:
        # Alert the user and redirect to a subscription management page
        messages.warning(
            request, 
            f"You are already subscribed to the {plan.plan_name} plan. Consider upgrading to a higher plan for more benefits!"
        )
        return redirect('view_subscriptions_plans_user')  # Replace with your desired redirect URL

    # If no active subscription, create a new subscription
    end_date = timezone.now() + relativedelta(months=plan.duration)
    subscription = Subscriptions.objects.create(
        user=user,
        plan=plan,
        start_date=timezone.now(),
        end_date=end_date,
        status=3  # Initial status set to "pending"
    )

    return render(request, 'library/payment.html', {"subscription_id": subscription})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Payment, Subscriptions

def process_payment(request):
    user=request.user
    if request.method == "POST":
        payment_method = request.POST.get('payment_method')
        subscription_id = request.POST.get('subscription_id')  # Assuming the subscription ID is passed in the form
        subscription = get_object_or_404(Subscriptions, id=subscription_id)

        try:
            # Mock payment processing logic (you'd integrate an actual payment gateway here)
            if payment_method == "credit_card":
                card_number = request.POST.get('card_number')
                expiry_date = request.POST.get('expiry_date')
                cvv = request.POST.get('cvv')
                # Perform credit card payment validation and processing here
                
            elif payment_method == "google_pay":
                # Handle Google Pay logic here
                pass
            
            elif payment_method == "bank_transfer":
                bank_account_number = request.POST.get('bank_account_number')
                bank_name = request.POST.get('bank_name')
                transfer_ref = request.POST.get('bank_transfer_ref')
                # Perform bank transfer validation and processing here
            
            # Save the payment details to the Payment model
            payment = Payment.objects.create(
                amount=subscription.plan.price,  # Assuming plan price is the payment amount
                payment_type=payment_method,
                user=subscription.user
            )
            payment.save()
            active_subscription = Subscriptions.objects.filter(user=user, end_date__gte=now(), status=1).first()
            
            
            if active_subscription:
                active_subscription.status=2
                active_subscription.save()
            
            # Update subscription status to "Active"
            subscription.status = 1  # Status "1" corresponds to "Active"
            subscription.save()

            messages.success(request, f"Payment successfully processed! Your subscription to {subscription.plan.plan_name} is now active.")
            return redirect('home_path')  # Redirect to a success page or home page
        
        except Exception as e:
            # Handle payment failure
            messages.error(request, f"Payment failed: {str(e)}")
            return redirect('home_path')  # Redirect to an error page

    


    

# def view_subscriptions_plan_user(request):
#     user = request.user

#     # Check if the user has an active subscription
#     active_subscription = Subscriptions.objects.filter(
#         user=user,
#         status=1,  # Active status
#         end_date__gte=now()  # Ensure the subscription is still valid
#     ).first()

#     if active_subscription:
#         # Redirect to upgrade plan with a message
#         messages.info(
#             request,
#             f"You currently have an active subscription plan: {active_subscription.plan.plan_name}. "
#             "Would you like to upgrade to a higher plan?"
#         )
#         return redirect('upgrade_plan')  # Redirect to the upgrade plan view

#     # If no active subscription, show all subscription plans
#     subscriptions_list = SubscriptionPlans.objects.prefetch_related('plans__category').all()
#     return render(request, 'library/view_subscriptions_plans_user.html', {
#         'subscriptions_list': subscriptions_list
#     })
      
    




from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Subscriptions, SubscriptionPlans

# def view_subscriptions_plan_user(request):
#     user = request.user

#     # Check if the user has an active subscription
#     active_subscription = Subscriptions.objects.filter(
#         user=user,
#         status=1,  # Active status
#         end_date__gte=now()  # Ensure the subscription is still valid
#     ).first()

#     if active_subscription:
#         # Redirect to upgrade plan with a message
#         messages.info(
#             request,
#             f"You currently have an active subscription plan: {active_subscription.plan.plan_name}. "
#             "Would you like to upgrade to a higher plan?"
#         )
#         return redirect('upgrade_plan')  # Redirect to the upgrade plan view

#     # If no active subscription, show all subscription plans
#     subscriptions_list = SubscriptionPlans.objects.prefetch_related('plans__category').all()
#     return render(request, 'library/view_subscriptions_plans_user.html', {
#         'subscriptions_list': subscriptions_list
#     })

# def view_subscriptions_plan_user(request):
#     user = request.user

#     # Check if the user has an active subscription
#     active_subscription = Subscriptions.objects.filter(
#         user=user,
#         status=1,  # Active status
#         end_date__gte=now()  # Ensure the subscription is still valid
#     ).first()

#     highest_plan = SubscriptionPlans.objects.order_by('-price').first()

#     if active_subscription:
#         # Check if the user has the highest plan
#         if active_subscription.plan == highest_plan:
#             alert_message = f"You already have the highest plan: {active_subscription.plan.plan_name}."
#         else:
#             alert_message = f"You currently have an active plan: {active_subscription.plan.plan_name}. Upgrade to a higher plan to access more features!"
#     else:
#         alert_message = "No active subscription. Subscribe to a plan to enjoy the benefits."

#     # Fetch all subscription plans for display
#     subscriptions_list = SubscriptionPlans.objects.all()

#     return render(request, 'library/view_subscriptions_plans_user.html', {
#         'subscriptions_list': subscriptions_list,
#         'active_subscription': active_subscription,
#         'alert_message': alert_message,
#         'highest_plan': highest_plan,
#     })



from django.shortcuts import render
from .models import SubscriptionPlans

# def upgrade_plan(request):
#     # Fetch higher plans for display
#     upgradeable_plans = SubscriptionPlans.objects.all()
#     return render(request, 'library/upgrade_plan.html', {
#         'upgradeable_plans': upgradeable_plans
#     })



#---------testing code---------------------
@login_required
def view_subscriptions_plan_user(request):
    user = request.user
    active_subscription = Subscriptions.objects.filter(user=user, end_date__gte=now(), status=1).first()
    # subscription = SubscriptionPlans.objects.all()

    if active_subscription:
        # Fetch higher plans
        upgradeable_plans = SubscriptionPlans.objects.filter(price__gt=active_subscription.plan.price)
        
    else:
        upgradeable_plans = SubscriptionPlans.objects.all()
        print(upgradeable_plans)


    context = {
         'active_subscription': active_subscription,
        'upgradeable_plans': upgradeable_plans,
        # 'subscription_plan' : subscription
    }    
    return render(request, 'library/view_subscriptions_plans_user.html', context)
    
    
    
    #         'active_subscription': active_subscription,
    #         'higher_plans': higher_plans,
    #     })
    # else:
    #     # User has no active subscriptions, show all available plans
    #     subscriptions_list = SubscriptionPlans.objects.all()
    #     return render(request, 'library/view_subscriptions_plans_user.html', {
    #         'subscriptions_list': subscriptions_list,
    #     })
    



# @login_required
# def upgrade_plan(request, pk):
#     user = request.user
#     plan_to_upgrade = get_object_or_404(SubscriptionPlans, id=pk)
#     active_subscription = Subscriptions.objects.filter(user=user, end_date__gte=now(), status=1).first()

#     if not active_subscription:
#         messages.info(request, "You do not have an active subscription to upgrade.")
#         return redirect('view_subscriptions_plans_user')

#     if plan_to_upgrade.price <= active_subscription.plan.price:
#         messages.error(request, "You cannot downgrade or select a similar plan.")
#         return redirect('view_subscriptions_plans_user')

#     if request.method == "POST":
#         # Mark the current plan as expired
#         active_subscription.status = 2  # Expired
#         active_subscription.save()

#         # Add the new subscription
#         new_subscription = Subscriptions.objects.create(
#             user=user,
#             plan=plan_to_upgrade,
#             start_date=now(),
#             end_date=now() + relativedelta(months=plan_to_upgrade.duration),
#             status=1  # Active
#         )

#         messages.success(request, f"Successfully upgraded to the {plan_to_upgrade.plan_name} plan!")
#         return redirect('view_subscriptions_plans_user')

#     return render(request, 'library/upgrade_prompt.html', {
#         'plan_to_upgrade': plan_to_upgrade,
#         'active_subscription': active_subscription
#     })



# @login_required
# def upgrade_plan(request, pk):
#     user = request.user
#     plan_to_upgrade = get_object_or_404(SubscriptionPlans, id=pk)
#     active_subscription = Subscriptions.objects.filter(user=user, end_date__gte=now(), status=1).first()

#     if not active_subscription:
#         messages.info(request, "You do not have an active subscription to upgrade.")
#         return redirect('view_subscriptions_plans_user')

#     if plan_to_upgrade.price <= active_subscription.plan.price:
#         messages.error(request, "You cannot downgrade or select a similar plan.")
#         return redirect('view_subscriptions_plans_user')

#     if request.method == "POST":
#         # Mark the current plan as expired
#         active_subscription.status = 2  # Expired
#         active_subscription.save()

#         # Add the new subscription
#         new_subscription = Subscriptions.objects.create(
#             user=user,
#             plan=plan_to_upgrade,
#             start_date=now(),
#             end_date=now() + relativedelta(months=plan_to_upgrade.duration),
#             status=1  # Active
#         )

#         messages.success(request, f"Successfully upgraded to the {plan_to_upgrade.plan_name} plan!")
#         return redirect('view_subscriptions_plans_user')

#     return render(request, 'library/upgrade_prompt.html', {
#         'plan_to_upgrade': plan_to_upgrade,
#         'active_subscription': active_subscription
#     })


# @login_required
# def upgrade_plan(request, pk):
#     user = request.user
#     plan_to_upgrade = get_object_or_404(SubscriptionPlans, id=pk)
#     active_subscription = Subscriptions.objects.filter(user=user, end_date__gte=now(), status=1).first()

#     if not active_subscription:
#         messages.info(request, "You do not have an active subscription to upgrade.")
#         return redirect('view_subscriptions_plans_user')

#     # Check if the selected plan is the same or lower than the current plan
#     if plan_to_upgrade.price <= active_subscription.plan.price:
#         messages.info(request, "You do not have any higher plans.")
#         return redirect('view_subscriptions_plans_user')

#     if request.method == "POST":
#         # Mark the current plan as expired
#         active_subscription.status = 2  # Expired
#         active_subscription.save()

#         # Add the new subscription
#         new_subscription = Subscriptions.objects.create(
#             user=user,
#             plan=plan_to_upgrade,
#             start_date=now(),
#             end_date=now() + relativedelta(months=plan_to_upgrade.duration),
#             status=1  # Active
#         )

#         messages.success(request, f"Successfully upgraded to the {plan_to_upgrade.plan_name} plan!")
#         return redirect('view_subscriptions_plans_user')

#     return render(request, 'library/upgrade_prompt.html', {
#         'plan_to_upgrade': plan_to_upgrade,
#         'active_subscription': active_subscription
#     })


# @login_required
# def upgrade_plan(request, pk=None):
#     user = request.user

#     # Get the user's active subscription
#     active_subscription = Subscriptions.objects.filter(user=user, end_date__gte=now(), status=1).first()

#     if not active_subscription:
#         # If no active subscription, show the list of plans
#         available_plans = SubscriptionPlans.objects.all()
#         messages.info(request, "You do not have an active subscription. Please choose a plan.")
#         return render(request, 'library/view_subscription.html', {'available_plans': available_plans})

#     # If a plan ID is provided, fetch the plan to upgrade
#     plan_to_upgrade = None
#     if pk:
#         plan_to_upgrade = get_object_or_404(SubscriptionPlans, id=pk)

#         # Prevent downgrades or selecting a similar plan
#         if plan_to_upgrade.price <= active_subscription.plan.price:
#             messages.error(request, "You cannot downgrade or select a similar plan.")
#             return redirect('view_subscriptions_plans_user')

#         if request.method == "POST":
#             # Expire the current plan
#             active_subscription.status = 2  # Expired
#             active_subscription.save()

#             # Create a new subscription
#             Subscriptions.objects.create(
#                 user=user,
#                 plan=plan_to_upgrade,
#                 start_date=now(),
#                 end_date=now() + relativedelta(months=plan_to_upgrade.duration),
#                 status=1  # Active
#             )

#             messages.success(request, f"Successfully upgraded to the {plan_to_upgrade.plan_name} plan!")
#             return redirect('view_subscriptions_plans_user')

#     return render(request, 'library/upgrade_prompt.html', {
#         'plan_to_upgrade': plan_to_upgrade,
#         'active_subscription': active_subscription
#     })


# @login_required
# def upgrade_plan(request, pk):
#     user = request.user
#     plan_to_upgrade = get_object_or_404(SubscriptionPlans, id=pk)
#     active_subscription = Subscriptions.objects.filter(user=user, end_date__gte=now(), status=1).first()

#     if not active_subscription:
#         messages.info(request, "You do not have an active subscription to upgrade.")
#         return redirect('view_subscriptions_plans_user')

#     # Check if the selected plan is the same or lower than the current plan
#     if plan_to_upgrade.price <= active_subscription.plan.price:
#         messages.info(request, "You do not have any higher plans.")
#         return redirect('view_subscriptions_plans_user')

#     if request.method == "POST":
#         # Mark the current plan as expired
#         active_subscription.status = 2  # Expired
#         active_subscription.save()

#         # Add the new subscription
#         new_subscription = Subscriptions.objects.create(
#             user=user,
#             plan=plan_to_upgrade,
#             start_date=now(),
#             end_date=now() + relativedelta(months=plan_to_upgrade.duration),
#             status=1  # Active
#         )

#         messages.success(request, f"Successfully upgraded to the {plan_to_upgrade.plan_name} plan!")
#         return redirect('view_subscriptions_plans_user')

#     return render(request, 'library/payment.html', {
#         'plan_to_upgrade': plan_to_upgrade,
#         'active_subscription': active_subscription,
        
#     })


# original

# @login_required
# def confirm_subscription(request, pk):
#     plan_to_confirm = get_object_or_404(SubscriptionPlans, id=pk)
#     # Add logic for confirming subscription, e.g., processing the payment

#     # After confirmation, create a new subscription for the user
#     user = request.user
#     new_subscription = Subscriptions.objects.create(
#         user=user,
#         plan=plan_to_confirm,
#         start_date=now(),
#         end_date=now() + relativedelta(months=plan_to_confirm.duration),
#         status=1  # Active
#     )
#     new_subscription.save()
#     messages.success(request, f"Successfully upgraded to the {plan_to_confirm.plan_name} plan!")
#     return redirect('view_subscriptions_plans_user')


@login_required
def confirm_subscription(request, pk):
    plan_to_confirm = get_object_or_404(SubscriptionPlans, id=pk)
    user = request.user

    # Mark the current active subscription as expired
    active_subscription = Subscriptions.objects.filter(user=user, end_date__gte=now(), status=1).first()
    if active_subscription:
        active_subscription.status = 2  # Expired
        active_subscription.save()

    # Create the new subscription
    new_subscription = Subscriptions.objects.create(
        user=user,
        plan=plan_to_confirm,
        start_date=now(),
        end_date=now() + relativedelta(months=plan_to_confirm.duration),
        status=1  # Active
    )
    new_subscription.save()

    messages.success(request, f"Successfully subscribed to the {plan_to_confirm.plan_name} plan!")
    return redirect('view_subscriptions_plans_user')



# @login_required
# def upgrade_plan(request, pk):
#     user = request.user
#     plan_to_upgrade = get_object_or_404(SubscriptionPlans, id=pk)
#     active_subscription = Subscriptions.objects.filter(user=user, end_date__gte=now(), status=1).first()

#     if not active_subscription:
#         messages.info(request, "You do not have an active subscription to upgrade.")
#         return redirect('view_subscriptions_plans_user')

#     # Check if the selected plan is the same or lower than the current plan
#     if plan_to_upgrade.price <= active_subscription.plan.price:
#         messages.info(request, "You do not have any higher plans.")
#         return redirect('view_subscriptions_plans_user')

#     # Redirect to payment page for processing
#     if request.method == "POST":
#         # Create a temporary "pending" subscription for the upgraded plan
#         end_date = now() + relativedelta(months=plan_to_upgrade.duration)

#         new_subscription = Subscriptions.objects.create(
#             user=user,
#             plan=plan_to_upgrade,
#             start_date=now(),
#             end_date=end_date,
#             status=3  # Pending until payment is successful
#         )

#         return render(request, 'library/payment.html', {"subscription_id": new_subscription.id})

#     return render(request, 'library/upgrade_prompt.html', {
#         'plan_to_upgrade': plan_to_upgrade,
#         'active_subscription': active_subscription
#     })


# @login_required
# def upgrade_plan(request, pk):
#     user = request.user
#     plan_to_upgrade = get_object_or_404(SubscriptionPlans, id=pk)
#     active_subscription = Subscriptions.objects.filter(user=user, end_date__gte=now(), status=1).first()

#     if not active_subscription:
#         messages.info(request, "You do not have an active subscription to upgrade.")
#         return redirect('view_subscriptions_plans_user')

#     # Check if the selected plan is the same or lower than the current plan
#     if plan_to_upgrade.price <= active_subscription.plan.price:
#         messages.info(request, "You do not have any higher plans.")
#         return redirect('view_subscriptions_plans_user')

#     # Redirect to payment page for processing
#     if request.method == "POST":
#         # Create a temporary "pending" subscription for the upgraded plan
#         end_date = now() + relativedelta(months=plan_to_upgrade.duration)

#         new_subscription = Subscriptions.objects.create(
#             user=user,
#             plan=plan_to_upgrade,
#             start_date=now(),
#             end_date=end_date,
#             status=3  # Pending until payment is successful
#         )

#         return render(request, 'library/payment.html', {"subscription_id": new_subscription.id})

#     return render(request, 'library/upgrade_prompt.html', {
#         'plan_to_upgrade': plan_to_upgrade,
#         'active_subscription': active_subscription
#     })



# @login_required
# def upgrade_plan(request, pk):
#     user = request.user
#     plan_to_upgrade = get_object_or_404(SubscriptionPlans, id=pk)
#     active_subscription = Subscriptions.objects.filter(user=user, end_date__gte=now(), status=1).first()

#     if not active_subscription:
#         messages.info(request, "You do not have an active subscription to upgrade.")
#         return redirect('view_subscriptions_plans_user')

#     # Check if the selected plan is the same or lower than the current plan
#     if plan_to_upgrade.price <= active_subscription.plan.price:
#         messages.info(request, "You cannot upgrade to a plan with equal or lower value.")
#         return redirect('view_subscriptions_plans_user')

#     # Process upgrade
#     if request.method == "POST":
#         # Mark the current subscription as expired
#         active_subscription.status = 2  # Assuming 2 represents 'Expired'
#         active_subscription.save()

#         # Create a new subscription for the upgraded plan
#         end_date = now() + relativedelta(months=plan_to_upgrade.duration)

#         new_subscription = Subscriptions.objects.create(
#             user=user,
#             plan=plan_to_upgrade,
#             start_date=now(),
#             end_date=end_date,
#             status=1  # Active
#         )
#         new_subscription.save()

#         messages.success(request, f"Successfully upgraded to the {plan_to_upgrade.plan_name} plan!")
#         return redirect('view_subscriptions_plans_user')

#     return render(request, 'library/upgrade_prompt.html', {
#         'plan_to_upgrade': plan_to_upgrade,
#         'active_subscription': active_subscription
#     })


@login_required
def upgrade_plan(request, pk):
    user = request.user
    plan_to_upgrade = get_object_or_404(SubscriptionPlans, id=pk)
    active_subscription = Subscriptions.objects.filter(user=user, end_date__gte=now(), status=1).first()

    if not active_subscription:
        messages.info(request, "You do not have an active subscription to upgrade.")
        return redirect('view_subscriptions_plans_user')

    # Check if the selected plan is higher than the current plan
    if plan_to_upgrade.price <= active_subscription.plan.price:
        messages.info(request, "You cannot upgrade to a plan with equal or lower value.")
        return redirect('view_subscriptions_plans_user')


    return render(request, 'library/upgrade_prompt.html', {
        'plan_to_upgrade': plan_to_upgrade,
        'active_subscription': active_subscription
    })


# def subscription_home(request):
#     subscription = SubscriptionPlans.objects.all()
#     return render(request,'library/subscription_home.html',{'subscription':subscription})



@login_required
def subscription_home(request):
    # Check if the user has an active subscription
    active_subscription = Subscriptions.objects.filter(user=request.user, status= 1).first()
    
    if active_subscription:
        # If the user has an active subscription, redirect to their subscription management page
        return redirect('view_subscriptions_plans_user')  # Replace with the actual URL name for subscription management
    else:
        # If no active subscription, show available plans
        available_plans = SubscriptionPlans.objects.all()  # or any filter you need
        return render(request, 'library/subscription_home.html', {'subscription': available_plans})
    

@login_required
def purchase_book(request, pk):
    book = get_object_or_404(Book, id=pk)

    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')  # Retrieve selected payment type
        
        if not payment_type:
            messages.error(request, "Please select a payment method.")
            return render(request, 'library/purchase_book.html', {'book': book})

        if book.stock_quantity > 0:  # Ensure there is stock available
            # Decrease the stock quantity
            book.stock_quantity -= 1
            book.save()

            # Create a payment record
            payment = Payment.objects.create(
                amount=book.price,
                payment_type=payment_type,  # Save the selected payment type
                user=request.user,
                payment_action=2  # Indicating a purchase action
            )

            # Success message and redirect
            messages.success(request, f"You have successfully purchased {book.book_title}. Payment ID: {payment.id}")
            return redirect('home_path')  # Redirect to a desired page after purchase
        else:
            # If no stock is available
            messages.error(request, f"Sorry, {book.book_title} is out of stock.")
            return redirect('home_path')

    return render(request, 'library/purchase_book.html', {'book': book})



    
from library.models import Notification

def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'library/notifications.html', {'notifications': user_notifications})


def notification_view(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()  # Assuming you have an `is_read` field

    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'library/topbar.html', context)

from .forms import AddCommentForm
def add_comment(request):
    if request.method=='POST':
        comment=AddCommentForm(request.POST)
        comment.save()
    else:
        comment=AddCommentForm()
    return render(request,'library/postdetails.html',{'comment_form':comment})

from .models import comments,Reviews      
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddCommentForm,AddReviewForm
from .models import Book, comments, Reviews

from django.contrib.auth.decorators import login_required  # Optional: To restrict access to logged-in users

@login_required
def book_view(request, pk):
    book = get_object_or_404(Book, id=pk)
    comment_list = comments.objects.filter(book_comments=book)
    reviews = Reviews.objects.filter(post=book)

    # Prepare star ranges for each review
    for review in reviews:
        review.filled_stars = range(review.rating)  # Range for filled stars
        review.empty_stars = range(5 - review.rating)  # Range for empty stars

    # Initialize forms for comments and reviews
    comment_form = AddCommentForm()
    review_form = AddReviewForm()

    if request.method == "POST":
        if "add_comment" in request.POST:  # Handle comment submission
            comment_form = AddCommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.book_comments = book
                new_comment.save()
                return redirect('view_book_details', pk=pk)
        elif "add_review" in request.POST:  # Handle review submission
            review_form = AddReviewForm(request.POST)
            if review_form.is_valid():
                new_review = review_form.save(commit=False)
                new_review.post = book
                new_review.review_author = request.user
                new_review.save()
                return redirect('view_book_details', pk=pk)

    return render(request, "library/book_view.html", {
        'book': book,
        "comm": comment_list,
        'reviews': reviews,
        'comment_form': comment_form,
        'review_form': review_form,
    })



def subscribe_upgrade(request,pk):
    user = request.user
    active_subscription = Subscriptions.objects.filter(user=user, end_date__gte=now(), status=1).first()
    new_plan=SubscriptionPlans.objects.get(id=pk)
    end_date = timezone.now() + relativedelta(months=new_plan.duration)
    subscription = Subscriptions.objects.create(
        user=user,
        plan=new_plan,
        start_date=timezone.now(),
        end_date=end_date,
        status=3  # Initial status set to "pending"
    )
    return render(request, 'library/payment.html', {"subscription_id": subscription})
