from django.urls import path
from .views import ChallengeListView, ChallengeDetailView

app_name = 'challenges'

urlpatterns = [
    path('', ChallengeListView.as_view(), name='challenge_list'),
    path('<int:pk>/', ChallengeDetailView.as_view(), name='challenge_detail'),
]
