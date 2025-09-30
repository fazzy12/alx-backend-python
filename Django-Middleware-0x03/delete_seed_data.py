import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "messaging_app.settings")
django.setup() 

from chats.models import User, Conversation, Message 

def delete_test_data():
    print("--- Deleting all test data ---")
    
    Message.objects.all().delete()
    Conversation.objects.all().delete()
    
    User.objects.filter(
        email__in=['user.a@test.com', 'user.b@test.com', 'intruder@test.com']
    ).delete()
    
    print("Test data cleared successfully.")

if __name__ == '__main__':
    delete_test_data()