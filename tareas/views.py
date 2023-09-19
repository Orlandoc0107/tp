from rest_framework import viewsets, generics, permissions
from .models import Tarea
from .serializers import TareaSerializer, UserRegistrationSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.http import HttpResponse
import json


#Todo en Uno xD!
class TareaViewSet(viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tarea.objects.filter(user=self.request.user)



# Vista de Registro
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Crea el usuario
        self.perform_create(serializer)
        user = serializer.instance

        token, created = Token.objects.get_or_create(user=user)

        response_data = {
            'message': 'Usuario creado exitosamente.',
            'token': token.key
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


# Login de Usuario
class UserLoginView(APIView):
    def post(self, request):
        dato1 = request.data.get('username')
        dato2 = request.data.get('password')
        usuario = authenticate(username=dato1, password=dato2)

        if usuario:
            key_usuario, created = Token.objects.get_or_create(user=usuario)

            data = {
                "id": usuario.id,
                "usuario": usuario.username,
                "nombre": usuario.first_name,
                "apellido": usuario.last_name,
                "email": usuario.email,
                "token": key_usuario.key,  
            }

            response = Response(data, status=status.HTTP_200_OK)
            
        
            response.set_cookie(key="auth_token", value=key_usuario.key)

            return response
        else:
            data = {"Error": "Credenciales Inválidas"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)