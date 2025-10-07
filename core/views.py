from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated,AllowAny    
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .utils import generate_verification_token, verify_token, send_verification_email



class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer

class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class CustomFieldViewSet(viewsets.ModelViewSet):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer

class EmailTemplateViewSet(viewsets.ModelViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer

class WorkflowTriggerViewSet(viewsets.ModelViewSet):
    queryset = WorkflowTrigger.objects.all()
    serializer_class = WorkflowTriggerSerializer

class DashboardView(APIView):
     # Allow any user (authenticated or not) to access this view
    def get(self, request):
        data = {
            'total_contacts': Contact.objects.count(),
            'total_leads': Contact.objects.filter(status='lead').count(),
            'total_clients': Contact.objects.filter(status='client').count(),
            'leads_by_stage': list(Opportunity.objects.values('stage').annotate(count=Count('id'))),
            'open_opportunities_value': Opportunity.objects.exclude(stage__in=['closed_won', 'closed_lost']).aggregate(total=Sum('deal_value'))['total'] or 0,
            'recent_interactions': list(Interaction.objects.order_by('-date')[:10].values('date', 'type', 'subject', 'summary')),
        }
        return Response(data)
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer    

#for login system

# User = get_user_model()

# @api_view(['POST'])
# def signup(request):
#     username = request.data.get('username')
#     email = request.data.get('email')
#     password = request.data.get('password')

#     if User.objects.filter(username=username).exists():
#         return Response({'error': 'Username already exists'}, status=400)
#     if User.objects.filter(email=email).exists():
#         return Response({'error': 'Email already registered'}, status=400)

#     user = User.objects.create_user(username=username, email=email, password=password)
#     user.is_active = False  # cannot login until verified
#     user.save()

#     token = generate_verification_token(email)
#     send_verification_email(email, token)

#     return Response({'message': 'Verification email sent! Please check your inbox.'}, status=201)

# @api_view(['GET'])
# def verify_email(request, token):
#     email = verify_token(token)
#     if not email:
#         return Response({'error': 'Invalid or expired token'}, status=400)
#     try:
#         user = User.objects.get(email=email)
#         user.is_active = True
#         user.is_verified = True
#         user.save()
#         return Response({'message': 'Email verified successfully! You can now log in.'})
#     except User.DoesNotExist:
#         return Response({'error': 'User not found'}, status=404)
    



#email verification system

@api_view(['GET'])
def verify_email(request, token):
    email = verify_token(token)
    if email:
        try:
            user = CustomUser.objects.get(email=email)
            if not user.is_verified:
                user.is_verified = True
                user.is_active = True  # Activate the user account
                user.save()
                return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Email already verified."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not all([username, email, password]):
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if CustomUser.objects.filter(email=email).exists():
        return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create inactive user
    user = CustomUser.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_active=False,  # User is inactive until verified
        is_verified=False
    )
    
    # Generate and send verification email
    token = generate_verification_token(email)
    send_verification_email(email, token)
    
    return Response({"message": "User created. Please check your email to verify."}, status=status.HTTP_201_CREATED)