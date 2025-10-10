from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import User, Message, MessageHistory
from django.db import connection
from django.db.models import Q



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
def message_list(request):
    """
    Demonstrates optimization (select_related) for a general message list/inbox query.
    """
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender', 'receiver').order_by('-timestamp')
    
    output_lines = [f"--- Optimized Message List for {request.user.email} ---"]
    output_lines.append(f"Total messages (first 5 shown): {len(messages)}")
    output_lines.append("---")

    for m in messages[:5]:
        output_lines.append(f"[{m.timestamp.strftime('%H:%M:%S')}] From: {m.sender.email} | To: {m.receiver.email} | Content: {m.content[:30]}...")
    
    output_lines.append("\n--- Optimization Summary ---")
    output_lines.append("Used select_related('sender', 'receiver') to eagerly fetch foreign key data, preventing the N+1 problem for listing messages.")

    return HttpResponse("\n".join(output_lines), status=200, content_type="text/plain")



@login_required
def message_thread(request, message_id):
    """
    Displays a message thread demonstrating optimized ORM techniques (Task 3).
    """
    
    try:
        initial_query_count = len(connection.queries)
        
        thread = Message.objects.get_thread_optimized(message_id) 
        
        list(thread) 
        final_query_count = len(connection.queries)
        
    except Message.DoesNotExist:
        if not Message.objects.filter(id=message_id).exists():
            raise Http404("Root message not found")
        thread = []
        final_query_count = initial_query_count 


    if not thread:
         return HttpResponse("Conversation not found or you are not authorized.", status=403)


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
    
    thread_display.append("\n--- ORM Optimization Used (Task 3) ---")
    thread_display.append("1. Custom Manager + Q() Object: Fetches root message and direct replies in a single query (recursive query implementation).")
    thread_display.append("2. select_related(): Used to eagerly fetch foreign key data (sender, receiver, parent_message) with one SQL JOIN, solving the N+1 issue.")


    return HttpResponse("\n".join(thread_display), status=200, content_type="text/plain")


@login_required
def unread_inbox(request):
    """
    Displays only unread messages using the custom manager's optimized query (Task 4).
    """
    unread_messages = Message.objects.unread_for_user(request.user)
    
    output_lines = [f"--- Unread Inbox for {request.user.email} ---"]
    output_lines.append(f"Total unread messages: {len(unread_messages)}")
    output_lines.append("---")
    for m in unread_messages:
        sender_email = m.sender.email 
        output_lines.append(f"From: {sender_email} | Read Status: {m.read} | Content: {m.content[:40]}...")

    output_lines.append("\n--- ORM Optimization Summary ---")
    output_lines.append("1. Custom Manager: Encapsulates business logic (`unread_for_user`).")
    output_lines.append("2. .only(): Used to retrieve only essential fields, reducing database load and memory usage.")

    return HttpResponse("\n".join(output_lines), status=200, content_type="text/plain")