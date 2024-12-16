from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

# Create your models here.
class Authors(models.Model):
    author_name = models.CharField(max_length=250)


    def __str__(self) :
        return self.author_name
    
class Category(models.Model):
    category_name = models.CharField(max_length=250)

    def __str__(self):
        return self.category_name
    
class Book(models.Model):
    ISBN = models.CharField(max_length=13, unique=True)
    book_title = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=550)
    hide_book  = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    stock_quantity = models.IntegerField()
    book_image =  models.ImageField(upload_to='library/images/')
    content_file = models.FileField(upload_to='library/books/', verbose_name="Book Content")
    publication_date = models.DateTimeField()
    author = models.ForeignKey(Authors,related_name="books",on_delete = models.CASCADE)
    category = models.ForeignKey(Category,related_name="books", on_delete=models.DO_NOTHING)


    def validate_pdf(value):
        if not value.name.endswith('.pdf'):
            raise ValidationError("Only PDF files are allowed.")

        def __str__(self):
            return self.book_title
    
class SubscriptionPlans(models.Model):
    plan_name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()

    def __str__(self):
        return self.plan_name
    
class Subscriptions(models.Model):
    plan_status =(
        (1,'Active'),
        (2,'Expired'),
        (3,'Pending')
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    plan = models.ForeignKey(SubscriptionPlans,related_name="plan_categories",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="plan_categories",on_delete=models.DO_NOTHING)
    status = models.PositiveSmallIntegerField(choices=plan_status,default=3)


    def __str__(self):
        return self.user.username
    

class PlanCategory(models.Model):
    plan = models.ForeignKey(SubscriptionPlans,related_name="plans", on_delete=models.CASCADE)
    category = models.ForeignKey(Category,related_name="plans",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.plan.plan_name} - {self.category.category_name}"
    

class Rent(models.Model):
    user = models.ForeignKey(User,related_name="rent_details",on_delete=models.CASCADE)
    book = models.ForeignKey(Book,related_name="rent_details",on_delete=models.CASCADE)
    rent_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField()


    def __str__(self):
        return f"{self.user.username}"
    


class Payment(models.Model):
    pay_type = (
        ('googlepay','Google Pay'),
        ('creditcard','Credit Card'),
        ('banktransfer','Bank Transfer')

    )

    pay_action = (
        (1,'Subscription'),
        (2,'Purchase'),
        (3,'Rent')
    )
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=50,choices=pay_type)
    user = models.ForeignKey(User,related_name='payment',on_delete=models.CASCADE)
    payment_action = models.PositiveSmallIntegerField(choices=pay_action,default=1)

    def __str__(self):
        return self.user.username
    

class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Notification for {self.user.username}: {self.message}"
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(max_length=150,blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Purchase(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.DO_NOTHING)
    date_added = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.user.username

class comments(models.Model):
    book_comments=models.ForeignKey(Book,on_delete=models.CASCADE)
    comment_text=models.TextField()
    comment_published_datetime=models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.comment_text
    
class Reviews(models.Model):
    stars=(
        (1,'one star'),
        (2,'two star'),
        (3,'three star'),
        (4,'four star'),
        (5,'five star')
    )
    post=models.ForeignKey(Book,related_name='review_of_book', on_delete=models.CASCADE)
    rating=models.PositiveSmallIntegerField(choices=stars,default=1)
    title=models.CharField(max_length=200)
    description =models.TextField(blank=True)
    review_author=models.ForeignKey(User,default=1 ,on_delete=models.CASCADE)

    def _str_(self):
        return self.title
    


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  # Prevent duplicate entries

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.book_title} - {self.quantity} pcs"

    def get_total_price(self):
        return self.book.price * self.quantity



# class Cart(models.Model):
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=10,decimal_places=2)
#     user = models.ForeignKey(User,related_name="user",on_delete=models.CASCADE)










# def edit_category(request,pk):
#     category_details = get_object_or_404(Category, id=pk)
#     # plan_details = get_object_or_404(PlanCategory,id = pk)

#     if request.method == 'POST':
#         edit_category = EditCategoryForm(request.POST or None,request.FILES or None,instance=category_details)

#         if edit_category.is_valid():
#             edit_category.save()

#             return redirect('view_category')
#         else:
#             print(edit_category.errors)
#     else:

#         edit_category  = EditCategoryForm(instance=category_details)
#     return render(request,'library/edit_category.html',{'edit_category_form':edit_category})
