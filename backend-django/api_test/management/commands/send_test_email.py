from django.core.mail import send_mail
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Send a test email to verify email configuration'

    def handle(self, *args, **kwargs):
        # Replace with your email address to receive the test email
        recipient_email = "oz@kstrainingacademy.com"

        try:
            send_mail(
                'Test Email from Django',
                'This is a test email to verify your email configuration.',
                'noreply@kstrainingacademy.com',  # Replace with DEFAULT_FROM_EMAIL
                [recipient_email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"Test email sent successfully to {recipient_email}!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to send test email: {e}"))