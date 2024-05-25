# courses/email_backends.py

from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings

class PhishingEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        kwargs['username'] = settings.PHISHING_EMAIL_HOST_USER
        kwargs['password'] = settings.PHISHING_EMAIL_HOST_PASSWORD
        kwargs['fail_silently'] = False
        super().__init__(*args, **kwargs)
