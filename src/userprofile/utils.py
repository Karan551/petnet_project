from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import string
import random
import time
from .models import AuthStatus
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

DEFAULT_EMAIL_FROM = "Petnet <noreply@petnet.com>"
WEBSITE_URL =settings.WEBSITE_URL
token = ""


def generate_token(length=64):
    characters = string.ascii_letters + string.digits

    return "".join(random.choice(characters) for _ in range(length))


def user_mail(request, subject, to_email):
    token = generate_token()

    # Set expiry time (15 minutes from now)
    token_expiry = timezone.now() + timedelta(minutes=15)

    # get user from user model
    user = User.objects.get(username=to_email)

    auth_user = None

    # create user status object
    try:
        # if user already have token then do this 
        auth_user = AuthStatus.objects.get(user_id=user.id)
        # print("this is user::",auth_user.user.username)
        
        
        if not auth_user.user.is_superuser:
            auth_user.reset_token = token
            auth_user.reset_token_expiry = token_expiry
            auth_user.save()
            
        
            
            
    except Exception as e:
        print('this is exception:', e)

    # if user first time came then do this
    if not auth_user:
        AuthStatus.objects.create(
            user=user, reset_token=token, reset_token_expiry=token_expiry)
    else:
        # if auth user is super user then do this
        auth_user.reset_token = token
        auth_user.reset_token_expiry = token_expiry
        auth_user.save()

    from_email = DEFAULT_EMAIL_FROM
    text_content = "reset your password"

    reset_link = f"{WEBSITE_URL}/userprofile/reset-password-confirm/?token={token}"

    html_content = render_to_string(
        "userprofile/password_reset_mail.html", {"reset_link": reset_link})

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        [to_email],
        headers={"List-Unsubscribe": "<mailto:noreply@petnet.com>"},
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
    time.sleep(5)
