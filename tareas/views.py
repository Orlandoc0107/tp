from rest_framework import viewsets, generics, permissions
from .models import Tarea
from .serializers import TareaSerializer, UserRegistrationSerializer
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response



class TareaViewSet(viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo permite al usuario ver y administrar sus propias tareas
        return Tarea.objects.filter(user=self.request.user)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class UserLoginView(APIView):
    def post(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response({'error': 'El usuario no está autenticado.'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})