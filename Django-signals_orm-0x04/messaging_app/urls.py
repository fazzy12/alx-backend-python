"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import messaging import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/delete/', views.delete_user, name='delete_user'),
    path('messages/<uuid:message_id>/history/', views.message_history,name='message_history'),
    path('messages/thread/<uuid:message_id>/', views.message_thread, name='message_thread'),
    path('messages/inbox/', views.message_list_optimized, name='message_list_optimized'),
]