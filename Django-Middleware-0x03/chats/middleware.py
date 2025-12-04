import os
from datetime import datetime
from django.conf import settings

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "AnonymousUser"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        
        log_file_path = os.path.join(settings.BASE_DIR, 'requests.log')
        
        try:
            with open(log_file_path, 'a') as f:
                f.write(log_message)
        except Exception:
            # Silently fail or log error in a production-safe way
            pass

        response = self.get_response(request)
        return response