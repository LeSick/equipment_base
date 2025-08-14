from django.urls import path
from .views import registration_request_view

app_name = 'accounts'

urlpatterns = [
    path('request-access/', registration_request_view, name='request_access'),
]