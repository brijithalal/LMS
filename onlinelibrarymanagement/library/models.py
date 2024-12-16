from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

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



   
class comments(models.Model):
    book_comments=models.ForeignKey(Book,on_delete=models.CASCADE)
    comment_text=models.TextField()
    comment_published_datetime=models.DateTimeField(auto_now_add=True)

    def __str__(self):
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

    def __str__(self):
        return self.title





