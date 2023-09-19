from django.db import models
from django.contrib.auth.models import User

#Creacin de Models de Tarea y se uso como ForeignKey el User de Django pro defecto

class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=1000)
    creado = models.DateTimeField(auto_now_add=True)
    finalizado = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['creado']

    def __str__(self):
        return self.titulo
