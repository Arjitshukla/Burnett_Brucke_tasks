from .models import AuditLog

# resuable Aduitlog function
def create_audit_log(request, event, details="", affected_object="", user=None, username=None):
    actor = user if user is not None else (
        request.user if request.user.is_authenticated else None
    )
    AuditLog.objects.create(
        username=username or (actor.username if actor else "Anonymous"),
        user=actor,
        event=event,
        affected_object=affected_object,
        details=details,
        ip_address=request.META.get('REMOTE_ADDR')
    )