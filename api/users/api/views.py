import jwt

from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import generics, viewsets
from rest_framework.response import Response
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

class CurrentUserView(generics.GenericAPIView):
    # This Works - I could probably get rid of the returned user data in my TokenObtainPair Serializer in the overwritten validate class
    def get(self, request):
        print('test', request.META.get('HTTP_AUTHORIZATION').split())
        # token = request.GET.get('token')
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        User = get_user_model()
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        print(payload)
        current_user = User.objects.get(id=payload['id'])
        print('current_user', current_user)
        serializer = UserSerializer(current_user)
        return Response(serializer.data)

    