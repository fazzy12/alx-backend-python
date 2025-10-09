from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import User, Message, MessageHistory 



@login_required
def delete_user(request):
    """
    Allows a logged-in user to delete their account.
    This triggers the post_delete signal for cleanup.
    """
    if request.method == 'POST':
        user_to_delete = request.user
        
        logout(request)

        user_to_delete.delete()
        
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