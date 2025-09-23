from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_hash', None)
        
        user = User.objects.create(**validated_data)
        
        user.set_password(password)
        user.save()
        
        return user

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    participants = UserSerializer(many=True, read_only=True)

    participants_emails = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True,
        required=True
    )
    
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'message_count', 'created_at', 'participants_emails']

    def get_message_count(self, obj):
        return obj.messages.count()

    def create(self, validated_data):
        participants_emails = validated_data.pop('participants_emails', [])
        
        conversation = Conversation.objects.create(**validated_data)
        
        for email in participants_emails:
            try:
                user = User.objects.get(email=email)
                conversation.participants.add(user)
            except User.DoesNotExist:
                raise serializers.ValidationError(f"User with email {email} does not exist.")
        
        return conversation
