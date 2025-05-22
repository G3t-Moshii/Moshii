from django.urls import path
from .views import GenerateCertificateView

app_name = 'certificates'

urlpatterns = [
    path('challenge/<int:challenge_id>/download/', GenerateCertificateView.as_view(), name='download_certificate'),
]
