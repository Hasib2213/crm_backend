from urllib.parse import quote
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from django.core.mail import send_mail
import os

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt='email-verify')

def verify_token(token, max_age=3600):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        token = token.replace('-', '.')  # Convert hyphens back to periods
        email = serializer.loads(token, salt='email-verify', max_age=max_age)
        return email
    except Exception:
        return None

def send_verification_email(email, token):
    safe_token = token.replace('.', '-')
    encoded_token = quote(safe_token)
    frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:5173')
    verify_link = f"{frontend_url}/verify-email/{encoded_token}"
    try:
        send_mail(
            subject="Verify your email",
            message=f"Click this link to verify your email: {verify_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
    except Exception as e:
        return False, str(e)
    return True, None