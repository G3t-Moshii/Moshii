from django.views.generic import ListView, DetailView
from .models import Course
from challenges.models import Challenge, UserChallengeAttempt # Import UserChallengeAttempt
from django.contrib.auth.mixins import LoginRequiredMixin # For user context

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(LoginRequiredMixin, DetailView): # Add LoginRequiredMixin
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        user = self.request.user
        
        challenges_in_course = Challenge.objects.filter(course=course)
        
        # Get completed challenges for the current user in this course
        completed_challenge_ids = []
        if user.is_authenticated:
            completed_challenge_ids = UserChallengeAttempt.objects.filter(
                user=user,
                challenge__in=challenges_in_course,
                is_successful=True
            ).values_list('challenge_id', flat=True)

        # Augment challenges with completion status
        challenges_with_status = []
        for challenge in challenges_in_course:
            challenges_with_status.append({
                'challenge': challenge,
                'is_completed': challenge.id in completed_challenge_ids
            })
        
        context['challenges_with_status'] = challenges_with_status
        context['total_challenges'] = challenges_in_course.count()
        context['completed_challenges_count'] = len(completed_challenge_ids)
        
        # Remove the old 'challenges' key if it exists to avoid confusion
        if 'challenges' in context:
            del context['challenges']
            
        return context
