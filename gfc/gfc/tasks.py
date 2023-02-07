from django.utils import timezone

from django.core.mail import send_mail



def testing():
    print("Sending Email")
    send_mail(
    'Subject here',
    'Here is the message.',
    'greggorfinancialcompanion@gmail.com',
    ['greggorfinancialcompanion@gmail.com'],
    fail_silently=False,
    )
    print("Sent")