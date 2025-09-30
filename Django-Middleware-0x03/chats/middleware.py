import os
from datetime import datetime
from django.http import HttpResponseForbidden

LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'requests.log')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        if not os.path.exists(LOG_FILE_PATH):
             with open(LOG_FILE_PATH, 'w') as f:
                 f.write(f"--- Log Started: {datetime.now()} ---\n")

    def __call__(self, request):
        
        response = self.get_response(request)

        user = str(request.user) if request.user.is_authenticated else 'Anonymous'
        
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"

        with open(LOG_FILE_PATH, 'a') as f:
            f.write(log_entry + '\n')
        
        return response


class RestrictAccessByTimeMiddleware:
    """
    Restricts access to the application between 9 PM and 6 AM.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now()
        current_hour = now.hour
            
        # Access is restricted if the time is 9 PM (21) or later, 
        # OR before 6 AM (6).
        if current_hour >= 21 or current_hour < 6:
            # Return a 403 Forbidden error
            return HttpResponseForbidden(
                "Access is restricted outside of 6:00 AM and 9:00 PM (server time)."
            )

        response = self.get_response(request)
        return response
