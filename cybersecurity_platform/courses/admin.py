from django.contrib import admin
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_premium', 'created_at', 'updated_at')
    list_filter = ('is_premium',)
    search_fields = ('title', 'description')

admin.site.register(Course, CourseAdmin)
