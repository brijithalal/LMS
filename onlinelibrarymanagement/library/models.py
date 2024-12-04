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
    ISBN = models.BigIntegerField()
    book_title = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=550)
    hide_book  = models.BooleanField(default=False)
    stock_quantity = models.IntegerField()
    publication_date = models.DateTimeField()
    author = models.ForeignKey(Authors,related_name="books",on_delete = models.CASCADE)
    category = models.ForeignKey(Category,related_name="books", on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.book_title
    
class SubscriptionPlans(models.Model):
    plan_name = models.CharField(max_length=250)
    duration = models.IntegerField()

    def __str__(self):
        return self.plan_name
    
class Subscriptions(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.ForeignKey(SubscriptionPlans,related_name="subscriptions",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="subscriptions",on_delete=models.DO_NOTHING)


    # def __str__(self):
    #     return self.user




