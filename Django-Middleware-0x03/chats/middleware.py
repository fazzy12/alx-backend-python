import os
from datetime import datetime

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