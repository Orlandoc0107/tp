from rest_framework import viewsets, status
from .models import Tarea
from .serializers import TareaSerializer, UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication  
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User





# Para ver Todas las Tareas 
class TareaViewSet(viewsets.ModelViewSet): # ModelViewSet se usa importando (from rest_framework import viewsets)
    queryset = Tarea.objects.all()  #especificar qué conjunto de datos se debe consultar de la base de datos
    serializer_class = TareaSerializer # eindicamos cuales son los datos que usaremos y estan serializados


#mostrar todas las Tareas 
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class MostarTareas(APIView):
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def get(self, request):
        tareas = Tarea.objects.filter(user=request.user).order_by('titulo')
        serializer = TareaSerializer(tareas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
    
# Crear Tarea
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CrearTarea(APIView):
    def post(self, request, format=None):
        serializer = TareaSerializer(data=request.data) 
        if serializer.is_valid(): 
            tarea = serializer.save(user=request.user)  # Asigna el usuario actual a la tarea
            return Response(TareaSerializer(tarea).data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Borrar Tarea

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BorrarTarea(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        tarea = Tarea.objects.filter(pk=pk, user=request.user).first()
        if not tarea:
            return Response({"error": "La tarea no existe o no tienes permiso para eliminarla"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TareaSerializer(tarea)
        tarea.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)




#Detallesde la tarea
# Detalles de la tarea
class DetallesTarea(APIView):
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def get(self, request, pk):
        tarea = Tarea.objects.filter(pk=pk, user=request.user).first()
        if not tarea:
            return Response({"error": "La tarea no existe o no tienes permiso para ver los detalles"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TareaSerializer(tarea)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#actualizar tarea
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ActualizarTarea(APIView):
    def put(self, request, pk):
        tarea = Tarea.objects.filter(pk=pk, user=request.user).first()
        if not tarea:
            return Response({"error": "La tarea no existe o no tienes permiso para actualizarla"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TareaSerializer(tarea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class Registro(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Verificar si el nombre de usuario y el correo electrónico ya están en uso
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Este nombre de usuario ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Este correo electrónico ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear el usuario si no hay errores de duplicación
            user = User.objects.create_user(
                username=username,
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                email=email,
                password=serializer.validated_data['password']
            )
            return Response({'message': 'Usuario creado exitosamente.'}, status=status.HTTP_201_CREATED)
        else:
            # Manejar errores de validación del serializador
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Login Envia el Token
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super(CustomTokenObtainPairView, self).post(request, *args, **kwargs)
        
        # Comprueba si la solicitud de inicio de sesión fue exitosa
        if response.status_code == status.HTTP_200_OK:
            # Extrae el token de acceso (access token) del cuerpo de la respuesta
            access_token = response.data.get('access', None)
            
            # Si se ha obtenido un token de acceso, devuélvelo en la respuesta personalizada
            if access_token:
                return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        
        # Si la solicitud de inicio de sesión no fue exitosa, devuelve la respuesta original
        return response
    

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class TokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        # Obtener el token de actualización de la solicitud
        refresh_token = request.data.get('refresh_token')

        # Comprobar si se proporcionó un token de actualización
        if not refresh_token:
            return Response({'error': 'Se requiere un token de actualización'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Intentar refrescar el token de acceso
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            # Devolver el nuevo token de acceso en la respuesta
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            # Manejar errores, por ejemplo, token de actualización inválido
            return Response({'error': 'No se pudo refrescar el token de acceso'}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Obtener_Datos(APIView):
    def get(self, request):
        user = request.user
        payload = {
            "usuario": user.username,
            "nombre": user.first_name,
            "apellido": user.last_name,
            "email": user.email,
        }
        return Response(payload, status=status.HTTP_200_OK)
