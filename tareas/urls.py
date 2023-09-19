# archivo creado , para las rutas

from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.urls import path, include
from .views import TareaViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TareaViewSet
from .views import UserRegistrationView
from django.urls import path
from .views import UserLoginView


router = routers.DefaultRouter()
router.register(r'tareas', TareaViewSet, basename='tarea')


urlpatterns = [
    path("", include(router.urls)),
    path('docs/', include_docs_urls(title="Argentina Programa API REST")),
    path('registro/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),

]