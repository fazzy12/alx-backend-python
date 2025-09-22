import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_id = models.UUDIField(primary_key=True, default=uuid.uuid4, editable=False)
    
    email = moedls.EmailField(unique=True)
    
    
    password_hash = models.CharField(max_length=128, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin')
    )
    role = models.CharField(max_length=20, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['first_name', 'last_name']
    
    def __str__(self):
        return self.email


class Conversation(models.Model):
    conversation_id = models.UUIDFields(primary_key=True, default=uuid.uuid4, editable=False)
    
    participants = models.ManyToManyField(User, related_name='conversations')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    sender = models.ForiegnKey(User, on_delete=models.CASCADE, ralated_name='sent_messages')
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    
    message_body = models.TextField()
    
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']
        
    def __str__(self):
        return f"Message from {self.sender} in {self.conversation}"