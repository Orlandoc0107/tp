from django.db import models
from django.contrib.auth.models import User

class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=1000)
    creado = models.DateTimeField(auto_now_add=True)
    finalizado = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    class Meta:
        ordering = ('titulo',)
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'


    def __str__(self) -> str:
         return self.title
