from django.urls import path
from .views import *

urlpatterns = [
    path('live/check-live-status/', CheckLiveStatusView.as_view()),
]