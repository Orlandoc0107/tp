# archivo creado , para las rutas

from django.urls import path, include
from rest_framework import routers
from tareas import views
from rest_framework.documentation import include_docs_urls



router = routers.DefaultRouter()
router.register(r'tareas', views.TareaView, 'tareas')

urlpatterns = [
    path("api/tp/", include(router.urls)),
    path('docs/', include_docs_urls(title="Argentina Programa API REST"))
]