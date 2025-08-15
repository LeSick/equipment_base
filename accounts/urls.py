from django.urls import path
from .views import registration_request_view
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('request-access/', registration_request_view, name='request_access'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=False
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='accounts:login',
        http_method_names=['get', 'post']
    ), name='logout'),
]