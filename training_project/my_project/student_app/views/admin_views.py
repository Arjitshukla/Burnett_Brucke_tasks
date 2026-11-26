from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from ..models import Student,Department, Course, UserProfile,AuditLog,Feedback, MarksUpdateHistory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from ..utils import create_audit_log
from ..decorators import role_required



# Admin_dashboard
@login_required
@role_required(['admin'])
def admin_dashboard(request):
    total_trainers = UserProfile.objects.filter(
        role='trainer'
    ).count()

    context = {
        'total_users': User.objects.count(),
        'total_students': Student.objects.count(),
        'total_courses': Course.objects.count(),
        'total_department': Department.objects.count(),
        'total_trainers': total_trainers,

        # 'recent_users': User.objects.order_by('-date_joined')[:5],
        'recent_users': User.objects.select_related('profile').order_by('-date_joined')[:5],
        'recent_students': Student.objects.order_by('-id')[:5],
        'recent_courses': Course.objects.order_by('-id')[:5],
    }

    return render(
        request,
        'students/dashboards/admin_dashboard.html',
        context 
    )


# TOGGLE FEEDBACK VISIBILITY
@login_required
@role_required(['admin'])
def toggle_feedback_visibility(request, feedback_id):
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")

    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.is_visible = not feedback.is_visible
    feedback.save()

    messages.success(request, "Feedback visibility updated.")
    return redirect('all_feedback')


# TOGGLE USER STATUS
@login_required
@role_required(['admin'])
def toggle_user_status(request, user_id):

    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")

    target_user = get_object_or_404(User, id=user_id)

    old_status = target_user.is_active

    target_user.is_active = not target_user.is_active
    target_user.save()

    new_status = target_user.is_active

    create_audit_log(
        request,
        "ACCOUNT_STATUS_CHANGE",
        f"Account status changed from {'Active' if old_status else 'Inactive'} to {'Active' if new_status else 'Inactive'}.",
        affected_object=f"User: {target_user.username}",
        user=request.user
    )

    messages.success(
        request,
        f"{target_user.username}'s account status updated successfully."
    )

    return redirect('admin_dashboard')



# AUDIT LOGS VIEW
@login_required
@role_required(['admin'])
def audit_logs_view(request):

    logs = AuditLog.objects.all().order_by('-timestamp')

    # Search
    search = request.GET.get('search', '').strip()
    if search:
        logs = logs.filter(
            Q(username__icontains=search) |
            Q(affected_object__icontains=search) |
            Q(details__icontains=search)
        )

    # Event filter
    event = request.GET.get('event', '')
    if event:
        logs = logs.filter(event=event)

    # Date range filter
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if start_date:
        logs = logs.filter(timestamp__date__gte=start_date)

    if end_date:
        logs = logs.filter(timestamp__date__lte=end_date)

    # Pagination
    paginator = Paginator(logs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'events': AuditLog.ACTION_CHOICES,
        'search': search,
        'selected_event': event,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(
        request,
        'students/audit_logs.html',
        context
    )


# All FEEDBACK VIEW
@login_required
@role_required(['admin'])
def all_feedback_view(request):
    feedbacks = Feedback.objects.select_related(
        'student', 'trainer', 'course'
    ).order_by('-created_at')

    return render(
        request,    
        'students/all_feedback.html',
        {'feedbacks': feedbacks}
    )


# MARKS HISTORY VIEW
@login_required
@role_required(['admin'])
def marks_history_view(request):

    history = MarksUpdateHistory.objects.select_related(
        'student',
        'course',
        'updated_by'
    ).order_by('-updated_at')

    context = {
        'history': history
    }

    return render(
        request,
        'students/marks_history.html',
        context
    )


