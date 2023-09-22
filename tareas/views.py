from rest_framework import viewsets, status, generics #, permissions
from .models import Tarea
from .serializers import TareaSerializer, UserRegistrationSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

# Para ver Todas las Tareas 
class TareaViewSet(viewsets.ModelViewSet): # ModelViewSet se usa importando (from rest_framework import viewsets)
    queryset = Tarea.objects.all()  #especificar qué conjunto de datos se debe consultar de la base de datos
    serializer_class = TareaSerializer # eindicamos cuales son los datos que usaremos y estan serializados




#mostrar todas las Tareas 
class MostarTareas(APIView): #APIView es un modulo que traeDjango para facilitar la Vistas en una APIREST.
    def get(self,request):
        tareas = Tarea.objects.all().order_by('titulo')
        serializer = TareaSerializer(tareas, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
# Crear Tarea
class CrearTarea(APIView):
    def post(self, request, format=None):
        serializer = TareaSerializer(data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Borrar Tarea
class BorrarTarea(APIView):
    def delete(self, request, pk):
        try:
            tarea = Tarea.objects.get(pk=pk)
            serializer = TareaSerializer(tarea)
            tarea.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tarea.DoesNotExist:
            return Response({"error": "La tarea no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#Detallesde la tarea
class DetallesTarea(APIView): 
    def get(self, request, pk): 
        tarea = Tarea.objects.filter(pk=pk).first()
        serializer = TareaSerializer(tarea) 
        if tarea: 
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    
#actualizar tarea
class ActualizarTarea(APIView):
    def put(self, request, pk):
        tarea = Tarea.objects.filter(pk=pk).first()
        serializer = TareaSerializer(tarea,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)



# Registro
# class Registro(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistrationSerializer
#     permission_classes = [AllowAny] # todos pueden ver el formulario o la vista

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         refresh = RefreshToken.for_user(user)
#         data = {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }

#         return Response(data, status=status.HTTP_201_CREATED)



#Ingresar
# class Login(TokenObtainPairView):
#     # Agrega cualquier lógica personalizada aquí, si es necesario
#     # Por ejemplo, puedes personalizar la respuesta JSON
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         # Aquí puedes modificar la respuesta JSON según tus necesidades
#         # Por ejemplo, agregar datos adicionales al JSON de respuesta
#         if response.status_code == 200:
#             user = self.user
#             response.data['user_id'] = user.id
#             response.data['email'] = user.email
#         return response
    
# Datos de usuario

# class Datos_user(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         user_data = {
#             'id': user.id,
#             'username': user.username,
#             'email': user.email,
#         }
#         return Response(user_data, status=status.HTTP_200_OK)
    
    
class Registro(generics.CreateAPIView):
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



# #Todo en Uno xD!
# class TareaViewSet(viewsets.ModelViewSet):
#     serializer_class = TareaSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Tarea.objects.filter(user=self.request.user)



# User = get_user_model()




#Login de Usuario
class Login(APIView):
    def post(self, request):
        dato1 = request.data.get('username')
        dato2 = request.data.get('password')
        usuario = authenticate(username=dato1, password=dato2)

        if usuario:

            data = {
                "id": usuario.id,
                "usuario": usuario.username,
                "nombre": usuario.first_name,
                "apellido": usuario.last_name,
                "email": usuario.email,  
            }

            response = Response(data, status=status.HTTP_200_OK)

            return response
        else:
            data = {"Error": "Credenciales Inválidas"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        


# class UserLoginView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         # Autenticar al usuario
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)  
#             response = super().post(request, *args, **kwargs)
#             if response.status_code == status.HTTP_200_OK:
                
#                 data = response.data
#                 data['id'] = user.id
#                 data['nombre'] = user.first_name
#                 data['apellido'] = user.last_name
#                 data['email'] = user.email
#                 return Response(data)
#             return response
#         else:
#             data = {"Error": "Credenciales Inválidas"}
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)