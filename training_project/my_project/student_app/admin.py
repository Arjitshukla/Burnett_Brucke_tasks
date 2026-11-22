from django.contrib import admin

# Register your models here.
from .models import Student, Department, StudentProfile, Course,UserProfile,AuditLog,Feedback,CourseMarks,MarksUpdateHistory

admin.site.register(Student)
admin.site.register(Department)
admin.site.register(StudentProfile)
admin.site.register(Course)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')   

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'username',
        'event',
        'affected_object',
        'ip_address',
        'timestamp',
    )

    list_filter = (
        'event',
        'timestamp',
    )

    search_fields = (
        'username',
        'details',
        'affected_object',
        'ip_address',
    )

    readonly_fields = (
        'username',
        'user',
        'event',
        'affected_object',
        'details',
        'ip_address',
        'timestamp',
    )

    ordering = ('-timestamp',)

admin.site.register(Feedback)
admin.site.register(CourseMarks)
admin.site.register(MarksUpdateHistory)