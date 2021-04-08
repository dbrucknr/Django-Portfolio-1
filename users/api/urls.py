from django.urls import path, include
from users.api.views import SignUpView, LogInView, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('sign_up/', SignUpView.as_view(), name='sign-up'),
    path('log_in/', LogInView.as_view(), name='log_in'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]