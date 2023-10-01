from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.contrib import admin 
from tareas import views
from tareas.views import MostarTareas, CrearTarea, BorrarTarea, ActualizarTarea, DetallesTarea
from tareas.views import Registro
from .views import CustomTokenObtainPairView, Obtener_Datos
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()
router.register(r'tareas', views.TareaViewSet, basename='tarea')

urlpatterns = [
       path('admin/', admin.site.urls),
       path('docs/', include_docs_urls(title="API Rest")),
       path('detalles-tarea/<int:pk>/', DetallesTarea.as_view()), #GET
       path('mostrar-tareas/', MostarTareas.as_view()), # GET
       path('crear-tarea/', CrearTarea.as_view()), # POST
       path('borrar-tarea/<int:pk>/', BorrarTarea.as_view()), # DELETE / pk= es la id de la tarea en la url
       path('actualiza-tarea/<int:pk>/', ActualizarTarea.as_view()), # PUT / pk= es id de la tarea en la url
       path('registro/', Registro.as_view(), name='register'), # POST
       path('token/', CustomTokenObtainPairView.as_view()), #POST
       path('datos/', Obtener_Datos.as_view()), #GET
]