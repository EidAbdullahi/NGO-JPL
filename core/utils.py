from django.core.exceptions import PermissionDenied

def require_role(user, *roles):
    if user.is_superuser:
        return
    if user.role not in roles:
        raise PermissionDenied("You do not have permission for this action.")
