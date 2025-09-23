from django.urls import path, include
from rest_framework.routers import DefaultRoutr
from .views import ConversationViewSet, MessageViewSet


router = DefaultRouter()


router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')


urlpartterns = [
    path('', include(router.urls)),
]