from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from library.models import Book, Notification

@receiver(post_save, sender=Book)
def notify_new_book(sender, instance, created, **kwargs):
    if created:  # Check if this is a new book
        message = f"A new book '{instance.book_title}' has been added to the library!"
        users = User.objects.all()  # Adjust to target specific users if needed
        for user in users:
            Notification.objects.create(user=user, message=message)