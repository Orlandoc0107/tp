# archivo creado , para las rutas

from django.urls import path, include
from rest_framework import routers
from tareas import views
from rest_framework.documentation import include_docs_urls
from . import views  
from rest_framework.authtoken.views import obtain_auth_token 



router = routers.DefaultRouter()
router.register(r'tareas', views.TareaView, 'tareas')

urlpatterns = [
    path("api/tp/", include(router.urls)),
    path('docs/', include_docs_urls(title="Argentina Programa API REST")),
    path('api/registro/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('api/iniciar-sesion/', obtain_auth_token, name='obtener_token'), 

]
