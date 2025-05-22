from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from challenges.models import UserChallengeAttempt, Challenge
from django.db.models import Sum # Not strictly needed if summing in Python

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get successfully completed challenges, ordered by most recent completion
        completed_attempts = UserChallengeAttempt.objects.filter(
            user=user,
            is_successful=True
        ).select_related('challenge', 'challenge__course').order_by('-completed_at')
        # select_related is to optimize fetching related Challenge and Course data

        context['completed_attempts'] = completed_attempts
        context['total_challenges_completed'] = completed_attempts.count()

        # Calculate total points from completed challenges
        # Assumes 'points' field is on the Challenge model
        total_points_earned = 0
        for attempt in completed_attempts:
            total_points_earned += attempt.challenge.points
        
        context['total_points_earned'] = total_points_earned
        
        # User's name for welcome message
        context['user_name'] = user.get_full_name() or user.username

        return context
