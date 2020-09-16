from django.urls import path

from .views import SendSMSAPIView

urlpatterns = [
    path('send-message/', SendSMSAPIView.as_view(), name='send-message'),
]
