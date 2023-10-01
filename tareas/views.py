from rest_framework import viewsets, status
from .models import Tarea
from .serializers import TareaSerializer, UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
# from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication  # Importa el módulo correcto
from rest_framework_simplejwt.views import TokenObtainPairView  # Importa la vista correcta

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
class BorrarTarea(APIView):
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
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
class ActualizarTarea(APIView):
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def put(self, request, pk):
        tarea = Tarea.objects.filter(pk=pk, user=request.user).first()
        if not tarea:
            return Response({"error": "La tarea no existe o no tienes permiso para actualizarla"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TareaSerializer(tarea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class Registro(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        user = serializer.instance

        user.is_staff = True
        user.save()

        response_data = {
            'message': 'Usuario creado exitosamente.',
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

# Obtener token JWT
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super(CustomTokenObtainPairView, self).post(request, *args, **kwargs)
        return response

# Obtener datos:
# Obtener datos del usuario logueado
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Obtener_Datos(APIView):
    def get(self, request):
        user = request.user
        payload = {
            "id": user.id,
            "usuario": user.username,
            "nombre": user.first_name,
            "apellido": user.last_name,
            "email": user.email,
        }
        return Response(payload, status=status.HTTP_200_OK)
    
    
#Login de Usuario
# class Login(APIView):
#     def post(self, request):
#         dato1 = request.data.get('username')
#         dato2 = request.data.get('password')
#         usuario = authenticate(username=dato1, password=dato2)

#         if usuario:

#             data = {
#                 "id": usuario.id,
#                 "usuario": usuario.username,
#                 "nombre": usuario.first_name,
#                 "apellido": usuario.last_name,
#                 "email": usuario.email,  
#             }

#             response = Response(data, status=status.HTTP_200_OK)

#             return response
#         else:
#             data = {"Error": "Credenciales Inválidas"}
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)
