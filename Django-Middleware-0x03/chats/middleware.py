import os
from datetime import datetime, timedelta
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


RPS_TRACKER = {}
MAX_MESSAGES_PER_MINUTE = 5
TIME_WINDOW_SECONDS = 60


# Helper function to get the client's true IP address
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
            
        if request.method == 'POST' and 'api/messages/' in request.path:
                
            ip_address = get_client_ip(request)
            now = datetime.now()
                
            min_time = now - timedelta(seconds=TIME_WINDOW_SECONDS)
                
            recent_requests = [
                t for t in RPS_TRACKER.get(ip_address, []) 
                if t > min_time
            ]
                
            if len(recent_requests) >= MAX_MESSAGES_PER_MINUTE:
                return HttpResponseForbidden(
                    f"Message limit exceeded. You can only send {MAX_MESSAGES_PER_MINUTE} messages per minute."
                )
                
            recent_requests.append(now)
            RPS_TRACKER[ip_address] = recent_requests
                
        response = self.get_response(request)
        return response


ALLOWED_ROLES = ['admin', 'host'] 


class RolePermissionMiddleware:
    """
    Checks the authenticated user's role and restricts access for non-privileged users
    on non-safe (modifying) HTTP methods.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
            

        if (request.user.is_authenticated and 
            request.method not in ('GET', 'HEAD', 'OPTIONS')):
                
            if request.user.role not in ALLOWED_ROLES:
                return HttpResponseForbidden(
                    f"Permission denied. Your role ({request.user.role}) is not authorized to perform this action."
                )


        response = self.get_response(request)
        return response