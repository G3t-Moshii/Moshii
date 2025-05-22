from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from challenges.models import Challenge, UserChallengeAttempt
# WeasyPrint will be imported dynamically if available
# If not, an error will be raised, which is acceptable for this setup phase.
# from weasyprint import HTML # Avoid top-level import if it causes issues on restricted envs

class GenerateCertificateView(LoginRequiredMixin, View):
    def get(self, request, challenge_id):
        challenge = get_object_or_404(Challenge, pk=challenge_id)
        user = request.user

        try:
            attempt = UserChallengeAttempt.objects.get(
                user=user,
                challenge=challenge,
                is_successful=True
            )
        except UserChallengeAttempt.DoesNotExist:
            return HttpResponseForbidden("You have not successfully completed this challenge, or the attempt was not recorded.")

        # Prepare context for the template
        context = {
            'user_name': user.get_full_name() or user.username,
            'challenge_name': challenge.title,
            'completion_date': attempt.completed_at,
        }
        
        html_string = render_to_string('certificates/certificate_template.html', context)

        try:
            from weasyprint import HTML
            # Added base_url to help WeasyPrint find static files if the template were to use them.
            # For this simple template, it might not be strictly necessary.
            html = HTML(string=html_string, base_url=request.build_absolute_uri('/')) 
            pdf = html.write_pdf()
        except ImportError:
            # Fallback or error if WeasyPrint is not available
            return HttpResponse("Error: PDF generation library (WeasyPrint) not found. Please ensure it is installed.", status=500)
        except Exception as e: # Catch other WeasyPrint errors
             return HttpResponse(f"Error generating PDF: {e}", status=500)


        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"certificate_{user.username}_{challenge.title.replace(' ', '_')}.pdf"
        # Make it inline for easier testing in browser, can be 'attachment' for download
        response['Content-Disposition'] = f'inline; filename="{filename}"' 
        
        return response
