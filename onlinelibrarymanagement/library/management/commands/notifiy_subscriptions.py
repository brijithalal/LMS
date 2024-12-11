from django.core.management.base import BaseCommand
from django.utils.timezone import now,timedelta
from library.models import Subscriptions, Notification

class Command(BaseCommand):
    help = 'Send reminders for subscriptions about to expire'

    def handle(self, *args, **kwargs):
        upcoming_expiry = now() + timedelta(days=3)  # Adjust days as needed
        expiring_subscriptions = Subscriptions.objects.filter(end_date__lte=upcoming_expiry, status=1)
        for subscription in expiring_subscriptions:
            message = f"Your subscription plan {subscription.plan.plan_name} will expire on {subscription.end_date}. Please renew it!"
            Notification.objects.create(user=subscription.user, message=message)
            self.stdout.write(f"Notification sent to {subscription.user.username}")