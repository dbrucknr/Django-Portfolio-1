from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from users.api.serializers import UserSerializer, LogInSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer