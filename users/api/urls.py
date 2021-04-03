from django.urls import path
from users.api.views import SignUpView, LogInView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='sign-up'),
    path('log_in/', LogInView.as_view(), name='log_in'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]