from urllib.parse import quote
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from django.core.mail import send_mail

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
    safe_token = token.replace('.', '-')  # Replace periods with hyphens
    encoded_token = quote(safe_token)  # URL-encode the modified token
    verify_link = f"http://localhost:5173/verify-email/{encoded_token}"
    send_mail(
        subject="Verify your email",
        message=f"Click this link to verify your email: {verify_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )