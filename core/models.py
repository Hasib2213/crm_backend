from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model

class Company(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    size_revenue = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    primary_contact = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, blank=True, related_name='primary_for')

    def __str__(self):
        return self.name

class Contact(models.Model):
    STATUS_CHOICES = [
        ('lead', 'Lead'),
        ('prospect', 'Prospect'),
        ('client', 'Client'),
    ]
    SOURCE_CHOICES = [
        ('referral', 'Referral'),
        ('web', 'Web'),
        ('cold_outreach', 'Cold Outreach'),
        ('other', 'Other'),
    ]
    full_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts')
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    role_title = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lead')
    last_contact_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.full_name

class Opportunity(models.Model):
    STAGE_CHOICES = [
        ('prospecting', 'Prospecting'),
        ('qualification', 'Qualification'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    ]
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='opportunities')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities')
    deal_name = models.CharField(max_length=255)
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, default='prospecting')
    deal_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expected_close_date = models.DateField(null=True, blank=True)
    probability = models.IntegerField(default=0)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <-- use this instead of User
        on_delete=models.SET_NULL,
        null=True,
        related_name='opportunities'
    )
    next_action = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.deal_name

class Interaction(models.Model):
    TYPE_CHOICES = [
        ('call', 'Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
    ]
    date = models.DateTimeField(auto_now_add=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='interactions')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='interactions')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    subject = models.CharField(max_length=255)
    summary = models.TextField()
    next_steps = models.TextField(blank=True)

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <-- use this instead of User
        on_delete=models.SET_NULL,
        null=True,
        related_name='tasks'
    )
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


class CustomField(models.Model):
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50)
    entity = models.CharField(max_length=50)

class EmailTemplate(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    body = models.TextField()

class WorkflowTrigger(models.Model):
    trigger_event = models.CharField(max_length=100)
    action = models.TextField()


class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)