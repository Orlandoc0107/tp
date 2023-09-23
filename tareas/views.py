from rest_framework import viewsets, status
from .models import Tarea
from .serializers import TareaSerializer, UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView

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
        