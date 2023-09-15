# aqui colocaremos quetipo de datos queremos enviar en fomato json ect ect ect 
from rest_framework import serializers
# importamos el serielizers 
from .models import Tarea


class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        #fields = ('id', 'titulo', 'descripcion', 'hecho')
        fields = '__all__'