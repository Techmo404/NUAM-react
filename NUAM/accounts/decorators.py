from functools import wraps
from django.http import JsonResponse

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "No autenticado"}, status=401)
        if request.user.role != "ADMIN":
            return JsonResponse({"error": "Solo admins pueden acceder"}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped


def employee_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "No autenticado"}, status=401)
        if request.user.role != "EMP":
            return JsonResponse({"error": "Solo empleados pueden acceder"}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped
