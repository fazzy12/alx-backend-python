from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


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