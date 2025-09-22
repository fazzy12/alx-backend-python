from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['user_id', 'firdt_name', 'last_name', 'email', 'phone_number', 'role', 'password']
        
        def create(self, validated_data):
            password  = validated_data.pop('password')
            validated_date.pop('password_hash', None)
        
        user = User.object.create(**validated_data)
        
        user.set_password(password)
        user.save()
        
        return user

class MessageSerializer(serializers.ModelSerializer):
    
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


class ConversationSerializeer(serializers.ModelSerializer):
    
    messages = MessageSerilizer(many=True, read_only=True)
    
    participants = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['converstion_id', 'participants', 'messages', 'created_at']
