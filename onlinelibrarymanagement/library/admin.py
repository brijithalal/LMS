from django.contrib import admin
from .models import Authors,Category,Book, PlanCategory,SubscriptionPlans,Subscriptions

# Register your models here.
admin.site.register(Authors)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(SubscriptionPlans)
admin.site.register(Subscriptions)
admin.site.register(PlanCategory)


