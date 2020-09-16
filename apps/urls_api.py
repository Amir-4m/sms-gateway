from django.urls import path, include

urlpatterns = [
    path('sms-gateway/', include("apps.gateway.api.urls")),
]
