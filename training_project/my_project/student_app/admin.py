from django.contrib import admin

# Register your models here.
from .models import Student, Department, StudentProfile, Course,UserProfile

admin.site.register(Student)
admin.site.register(Department)
admin.site.register(StudentProfile)
admin.site.register(Course)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')   