from django.core.mail import send_mail
from django.conf import settings
def send_email_to_client():
    subject = "this email from utopia"
    message = "hey"
    print("isd")
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["21101032@uap-bd.edu"]
    
    send_mail(subject,message,from_email,recipient_list)