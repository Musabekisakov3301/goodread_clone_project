from django.core.mail import send_mail
from main.celery import app

@app.task
def send_email(subject, message, recipient_list):
    send_mail(
                subject,
                message,
                'musabekisakov5@gmail.com',
                recipient_list
            )
