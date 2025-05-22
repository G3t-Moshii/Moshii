from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin # Import FormMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .models import Challenge, UserChallengeAttempt
from .forms import SolutionForm

class ChallengeListView(ListView):
    model = Challenge
    template_name = 'challenges/challenge_list.html'
    context_object_name = 'challenges'

class ChallengeDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Challenge
    template_name = 'challenges/challenge_detail.html'
    context_object_name = 'challenge'
    form_class = SolutionForm

    def get_success_url(self):
        return reverse('challenges:challenge_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        try:
            # Check if the user has a successful attempt for this challenge
            attempt = UserChallengeAttempt.objects.get(user=self.request.user, challenge=self.object, is_successful=True)
            context['completed_successfully'] = True
            context['completion_date'] = attempt.completed_at
        except UserChallengeAttempt.DoesNotExist:
            context['completed_successfully'] = False
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login') # Should be handled by LoginRequiredMixin

        self.object = self.get_object()
        form = self.get_form()

        # Check if already completed successfully
        if UserChallengeAttempt.objects.filter(user=request.user, challenge=self.object, is_successful=True).exists():
            messages.info(request, "You have already successfully completed this challenge.")
            return self.form_invalid(form) # Or redirect

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user_answer = form.cleaned_data['answer']
        challenge = self.object
        user = self.request.user

        # Get or create an attempt record (focusing on the first attempt or latest unsuccessful)
        # This logic might need refinement based on how you want to track multiple attempts vs one completion.
        attempt, created = UserChallengeAttempt.objects.get_or_create(
            user=user, 
            challenge=challenge,
            is_successful=False, # Look for an ongoing or new attempt
            defaults={'attempts_count': 0, 'submitted_answer': ''}
        )
        
        attempt.attempts_count += 1
        attempt.submitted_answer = user_answer

        # Basic flag checking (case-insensitive)
        # For more complex scenarios (quiz, lab), this logic will be different.
        is_correct = False
        if challenge.challenge_type == 'flag':
            is_correct = user_answer.lower() == challenge.solution_validator.lower()

        if is_correct:
            attempt.is_successful = True
            attempt.completed_at = timezone.now()
            attempt.save()
            # If there was a previous "is_successful=False" record for this user/challenge, 
            # it's now updated. If you want to keep all attempts, create new records.
            # For simplicity here, we are updating the existing one or the one created by get_or_create.

            # Award points (placeholder for future UserProfile update)
            # user.userprofile.points += challenge.points 
            # user.userprofile.save()

            messages.success(self.request, f"Correct! You've earned {challenge.points} points.")
            
            # If you want to create a new record for the successful attempt, distinct from prior unsuccessful ones:
            # UserChallengeAttempt.objects.create(
            #     user=user,
            #     challenge=challenge,
            #     is_successful=True,
            #     completed_at=timezone.now(),
            #     submitted_answer=user_answer,
            #     attempts_count=attempt.attempts_count # or a fresh count for this success
            # )
            # And potentially delete the `is_successful=False` record if you only want one record per user/challenge.
            # For now, the get_or_create with update is simpler for "one main attempt state".

        else:
            attempt.save() # Save the incremented attempt count and submitted answer
            messages.error(self.request, "Incorrect, please try again.")

        return super().form_valid(form)

    def form_invalid(self, form):
        # This might be called if the form itself is invalid (e.g. empty submission)
        # or if we call it manually after checking for existing completion.
        return self.render_to_response(self.get_context_data(form=form))
