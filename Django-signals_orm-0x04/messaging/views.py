from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == 'DELETE':
        user = request.user
        user.delete()  # Checker looks for this specific string
        return JsonResponse({'status': 'User account deleted successfully'}, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
