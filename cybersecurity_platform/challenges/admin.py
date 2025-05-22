from django.contrib import admin
from .models import Challenge, UserChallengeAttempt # Import UserChallengeAttempt

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'difficulty', 'challenge_type', 'points', 'created_at')
    list_filter = ('difficulty', 'challenge_type', 'course')
    search_fields = ('title', 'description')
    raw_id_fields = ('course',)

admin.site.register(Challenge, ChallengeAdmin)

class UserChallengeAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'is_successful', 'completed_at', 'attempts_count')
    list_filter = ('is_successful', 'challenge__course', 'user') # Filter by course via challenge
    search_fields = ('user__username', 'challenge__title')
    readonly_fields = ('completed_at',) # Typically set by the system

admin.site.register(UserChallengeAttempt, UserChallengeAttemptAdmin)
