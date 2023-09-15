from django.db import models

# Create your models here.

# clearmos clases
# y migramos  python manage.py makemigrations
# python manage.py migrate tareas
# python manage.py createsuperuser
class Tarea(models.Model):
    titulo = models.CharField(max_length=200) # le indicamos que sera tipo caracter maximo 200
    descripcion = models.TextField(blank=True) # blank=true para que pueda guardar tareas sin descripcion
    hecho = models.BooleanField(default=False) # tipo boleano y por defecto que se cree  falso


# agreagamos que datos poder ver

    def __str__(self):
        return self.titulo