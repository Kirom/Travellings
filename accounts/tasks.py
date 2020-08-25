import logging

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tokens import account_activation_token
from travel.celery import app


@app.task
def send_verification_email(user_id):
    user_model = get_user_model()
    try:
        user = user_model.objects.get(pk=user_id)
        mail_subject = f'Активация аккаунта на travellings.ml'
        message = render_to_string('accounts/acc_activation_email.html', {
            'user': user,
            'domain': 'travellings.ml',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
    except user_model.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
