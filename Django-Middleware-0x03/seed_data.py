import os
import django
from datetime import timedelta
from django.utils import timezone
import uuid

# 1. Initialize Django Environment FIRST
# This MUST happen before any code attempts to import models or access settings.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "messaging_app.settings")
django.setup() # <-- Triggers app loading using the settings file

# 2. Import Models AFTER setup is complete
from chats.models import User, Conversation, Message # <-- Imports moved here

# --- 3. Define Test Credentials ---
TEST_PASSWORD = "testpassword123"

def seed_data():
    
    print("--- Creating Test Users ---")
    
    # --- 4. Create Users (Passing email as first argument to satisfy UserManager) ---
    try:
        user_a = User.objects.create_user(
            'user.a@test.com', 
            password=TEST_PASSWORD,
            first_name='Alice',
            last_name='Smith',
            email='user.a@test.com'
        )
        print(f"Created User A: {user_a.email}")
    except Exception:
        user_a = User.objects.get(email='user.a@test.com')
        print(f"User A already exists. Fetching: {user_a.email}")

    # User B: Second Participant
    try:
        user_b = User.objects.create_user(
            'user.b@test.com', 
            password=TEST_PASSWORD,
            first_name='Bob',
            last_name='Jones',
            email='user.b@test.com'
        )
        print(f"Created User B: {user_b.email}")
    except Exception:
        user_b = User.objects.get(email='user.b@test.com')
        print(f"User B already exists. Fetching: {user_b.email}")

    # User C: Intruder (Non-Participant)
    try:
        user_c = User.objects.create_user(
            'intruder@test.com', 
            password=TEST_PASSWORD,
            first_name='Carl',
            last_name='Intruder',
            email='intruder@test.com'
        )
        print(f"Created User C (Intruder): {user_c.email}")
    except Exception:
        user_c = User.objects.get(email='intruder@test.com')
        print(f"User C already exists. Fetching: {user_c.email}")


    # --- 5. Create Conversation and Messages ---
    print("\n--- Creating Conversation and Messages ---")
    
    # Create Conversation
    try:
        conversation_1 = Conversation.objects.create()
        conversation_1.participants.add(user_a, user_b)
        print(f"Created Conversation 1: {conversation_1.conversation_id}")
        
        # Create Messages
        Message.objects.create(conversation=conversation_1, sender=user_a, message_body="Msg 1 from Alice", sent_at=timezone.now() - timedelta(minutes=5))
        Message.objects.create(conversation=conversation_1, sender=user_b, message_body="Msg 2 from Bob", sent_at=timezone.now() - timedelta(minutes=3))
        Message.objects.create(conversation=conversation_1, sender=user_a, message_body="Msg 3 from Alice (filter test)", sent_at=timezone.now())
        print(f"Created 3 messages in Conversation {conversation_1.conversation_id}")

    except Exception as e:
        print(f"Error creating conversation/messages. Check migrations: {e}")


if __name__ == '__main__':
    seed_data()
    print("\n--- Seeding Complete ---")
    print(f"Test Credentials: email/password = *user.a/b/intruder*@test.com / {TEST_PASSWORD}")