from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.contrib import admin 
from tareas import views
from tareas.views import MostarTareas, CrearTarea, BorrarTarea, ActualizarTarea, DetallesTarea
from tareas.views import Registro ,Login , Datos_user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
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
       path('registro/', Registro.as_view(), name='register'), 
       path('ingresar/', Login.as_view()),
       path('datos/',Datos_user.as_view()),
       path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # POST , esto es igual que el Login
       path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #POST ,
       path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'), #POST ,
]