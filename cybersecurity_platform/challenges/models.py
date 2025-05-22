from django.db import models
from courses.models import Course

class Challenge(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='challenges')
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    challenge_type = models.CharField(max_length=50, choices=[('flag', 'Flag-based'), ('quiz', 'Quiz'), ('lab', 'Lab Environment')])
    solution_validator = models.TextField() # Can store regex for flag, correct answers for quiz, or instructions for lab validation
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

from django.contrib.auth.models import User

class UserChallengeAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True, blank=True) # Set when successfully completed
    is_successful = models.BooleanField(default=False)
    submitted_answer = models.TextField(blank=True, null=True)
    attempts_count = models.IntegerField(default=0)

    class Meta:
        # Ensures a user can only have one primary "successful" attempt record per challenge.
        # If you want to track all attempts, remove this or adjust logic.
        # For now, this helps in easily identifying if a challenge is completed.
        unique_together = ('user', 'challenge', 'is_successful') 
        # A better approach for "one completion" might be a separate model or a flag on UserProfile

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} ({'Success' if self.is_successful else 'Attempted'})"
