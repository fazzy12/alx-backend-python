from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import User, Message, MessageHistory
from django.db import connection



@login_required
def delete_user(request):
    """
    Allows a logged-in user to delete their account.
    This triggers the post_delete signal for cleanup.
    """
    if request.method == 'POST':
        user = request.user
        
        logout(request)

        user.delete()
        
        return HttpResponse("Account deleted successfully.", status=200)
    
    return HttpResponse("Confirm account deletion. Send a POST request to this URL to permanently delete your account.", status=200)


@login_required
def message_history(request, message_id):
    """
    Displays the edit history for a specific message.
    """
    message = get_object_or_404(Message, id=message_id)
    
    if request.user != message.sender and request.user != message.receiver:
        return HttpResponse("You are not authorized to view this message history.", status=403)
        
    history = MessageHistory.objects.filter(message=message).order_by('-edited_at')
    
    if not history.exists():
        return HttpResponse(f"Message ID {message_id} has no edit history.", content_type="text/plain")

    history_lines = [f"Message History for ID: {message.id} (Current content: {message.content})", "-"*50]
    for entry in history:
        editor = entry.edited_by.email if entry.edited_by else 'Unknown User'
        history_lines.append(
            f"Previous content saved at: {entry.edited_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        history_lines.append(
            f"Edited by: {editor}"
        )
        history_lines.append(
            f"Previous Content: '{entry.old_content}'\n"
        )
        
    return HttpResponse("\n".join(history_lines), content_type="text/plain")


@login_required
def message_thread(request, message_id):
    """
    Displays a message thread using optimized ORM techniques.
    """
    try:
        initial_query_count = len(connection.queries)
        
        thread = Message.objects.get_thread(message_id) 
        
        list(thread)
        final_query_count = len(connection.queries)
        
    except Message.DoesNotExist:
        raise Http404("Root message not found")

    thread_display = [f"--- Optimized Message Thread (Root ID: {message_id}) ---"]
    thread_display.append(f"Queries executed for fetch (should be 1): {final_query_count - initial_query_count}")
    thread_display.append("--- Conversation ---")
    
    for m in thread:
        parent_id = str(m.parent_message.id) if m.parent_message else 'None (Root)'
        sender_email = m.sender.email 
        is_reply = 'REPLY -> ' if m.parent_message_id else 'ROOT: '

        thread_display.append(
            f"{is_reply}[{m.timestamp.strftime('%H:%M:%S')}] From: {sender_email} | Parent: {parent_id}"
        )
        thread_display.append(
            f"  Content: {m.content}"
        )
    
    thread_display.append("\n--- ORM Optimization Used ---")
    thread_display.append("1. Custom Manager: Encapsulates query logic (`get_thread`).")
    thread_display.append("2. Q() Object: Used in the query to fetch the parent and all direct replies in one step (simulating recursive threading at the first level).")
    thread_display.append("3. select_related(): Used to perform a single SQL JOIN to fetch foreign key objects (sender, receiver, parent_message), avoiding N+1 queries.")


    return HttpResponse("\n".join(thread_display), status=200, content_type="text/plain")
