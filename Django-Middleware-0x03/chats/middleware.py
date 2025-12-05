import os
from datetime import datetime
from django.conf import settings
from django.http import HttpResponseForbidden

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
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current hour (0-23)
        current_hour = datetime.now().hour

        # Define allowed hours (9 AM to 6 PM)
        # 9 AM is 9, 6 PM is 18
        start_hour = 9
        end_hour = 18

        # Logic: If current time is NOT between start and end, deny access
        if not (start_hour <= current_hour < end_hour):
            return HttpResponseForbidden("Access to the messaging app is restricted between 6 PM and 9 AM.")

        # If time is okay, proceed as normal
        response = self.get_response(request)
        return response