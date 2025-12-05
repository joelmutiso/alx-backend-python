import os
import time
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden

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
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to store IP request timestamps
        # Format: { '127.0.0.1': [time1, time2, ...] }
        self.ip_log = {}

    def __call__(self, request):
        # Only check rate limit for POST requests (sending messages)
        if request.method == 'POST':
            # Get user IP address
            ip_address = request.META.get('REMOTE_ADDR')
            current_time = time.time()
            
            # Initialize list for new IPs
            if ip_address not in self.ip_log:
                self.ip_log[ip_address] = []
            
            # Filter out timestamps older than 1 minute (60 seconds)
            # We keep only requests that happened in the last 60 seconds
            self.ip_log[ip_address] = [
                t for t in self.ip_log[ip_address] 
                if current_time - t < 60
            ]
            
            # Check if limit exceeded (5 messages per minute)
            if len(self.ip_log[ip_address]) >= 5:
                return JsonResponse(
                    {'error': 'Rate limit exceeded. Max 5 messages per minute.'}, 
                    status=429
                )
            
            # Log the current request
            self.ip_log[ip_address].append(current_time)

        response = self.get_response(request)
        return response
    
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define the roles that are allowed to perform actions
        allowed_roles = ['admin', 'moderator']

        # We only check permissions if the user is logged in
        if request.user.is_authenticated:
            # Get the user's role. 
            # getattr(obj, 'name', default) is safer than request.user.role 
            # in case the field is missing.
            user_role = getattr(request.user, 'role', 'guest')

            # If the user has a role, but it's not in the allowed list -> Block them
            if user_role not in allowed_roles:
                return HttpResponseForbidden(
                    "Access denied: You must be an admin or moderator to perform this action."
                )

        return self.get_response(request)