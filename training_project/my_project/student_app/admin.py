from django.contrib import admin

# Register your models here.
from .models import Student, Department, StudentProfile, Course,UserProfile,AuditLog

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

    list_display = ('id', 'username', 'event', 'timestamp')

    list_filter = ('event', 'timestamp')

    search_fields = ('username', 'event')

    readonly_fields = ('username', 'event', 'details', 'timestamp')