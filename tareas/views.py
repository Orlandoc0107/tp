from rest_framework import viewsets, generics, permissions
from .models import Tarea
from .serializers import TareaSerializer, UserRegistrationSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


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
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            error_message = str(e)
            response_data = {
                'error_message': error_message
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response_data = {
            'message': 'Usuario creado exitosamente.'
        }

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


# Login de Usuario
class UserLoginView(APIView):
    def post(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response({'error': 'El usuario no está autenticado.'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})