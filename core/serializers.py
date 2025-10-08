from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactSerializer(serializers.ModelSerializer):
    company_detail = serializers.StringRelatedField(source='company', read_only=True)

    class Meta:
        model = Contact
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    # Read-only nested detail for frontend display
    primary_contact = ContactSerializer(read_only=True)

    # Write-only field for form submission
    primary_contact_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        source='primary_contact',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'industry', 'size_revenue', 'address',
            'notes', 'primary_contact', 'primary_contact_id'
        ]


class OpportunitySerializer(serializers.ModelSerializer):
    contact = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all())
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), allow_null=True, required=False)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)

    contact_detail = serializers.StringRelatedField(source='contact', read_only=True)
    company_detail = serializers.StringRelatedField(source='company', read_only=True)
    owner_detail = serializers.StringRelatedField(source='owner', read_only=True)

    class Meta:
        model = Opportunity
        fields = '__all__'


class InteractionSerializer(serializers.ModelSerializer):
    contact_detail = serializers.StringRelatedField(source='contact', read_only=True)
    company_detail = serializers.StringRelatedField(source='company', read_only=True)

    class Meta:
        model = Interaction
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    owner_detail = serializers.StringRelatedField(source="owner", read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = '__all__'


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'


class WorkflowTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowTrigger
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
