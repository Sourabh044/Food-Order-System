<<<<<<< HEAD
=======
from email import message
>>>>>>> c64ac00cf1bee929791284b6fa6d91e088e004ab
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode

<<<<<<< HEAD

=======
>>>>>>> c64ac00cf1bee929791284b6fa6d91e088e004ab
def detectUser(user):
    if user.role == 1:
        redirecturl = "Vendor-Dashboard"
        return redirecturl
    elif user.role == 2:
        redirecturl = "Customer-Dashboard"
        return redirecturl
    elif user.role == None and user.is_superadmin:
        redirecturl = "/admin"
        return redirecturl


<<<<<<< HEAD
def send_verification_email(request, user, mail_subject, template_name):
=======
def send_verification_email(request, user,mail_subject,template_name):
>>>>>>> c64ac00cf1bee929791284b6fa6d91e088e004ab
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = mail_subject
    message = render_to_string(
        template_name,
        {
            user: user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.id)),
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email
<<<<<<< HEAD
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()


=======
    mail = EmailMessage(mail_subject, message,from_email, to=[to_email])
    mail.send()

>>>>>>> c64ac00cf1bee929791284b6fa6d91e088e004ab
# def send_password_reset_email(request,user):
#     from_email = settings.DEFAULT_FROM_EMAIL
#     current_site = get_current_site(request)
#     mail_subject = "Password Reset Email"
#     message = render_to_string(
#         "accounts/emails/account_password_reset_email.html",
#         {
#             user: user,
#             "domain": current_site,
#             "uid": urlsafe_base64_encode(force_bytes(user.id)),
#             "token": default_token_generator.make_token(user),
#         },
#     )
#     to_email = user.email
#     mail = EmailMessage(mail_subject, message,from_email, to=[to_email])
#     mail.send()


<<<<<<< HEAD
def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    mail_subject = mail_subject
    message = render_to_string(mail_template, context)
    to_email = context["user"].email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()
=======
def send_notification(mail_subject,mail_template,context):
    from_email = settings.DEFAULT_FROM_EMAIL
    mail_subject = mail_subject
    message = render_to_string(mail_template,context)
    to_email= context['user'].email
    mail = EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.send()
>>>>>>> c64ac00cf1bee929791284b6fa6d91e088e004ab
