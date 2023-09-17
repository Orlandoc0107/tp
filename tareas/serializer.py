# aqui colocaremos quetipo de datos queremos enviar en fomato json ect ect ect 
from rest_framework import serializers
from .models import Tarea
from django.contrib.auth.models import User


class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        #fields = ('id', 'titulo', 'descripcion', 'hecho')
        fields = '__all__'
        

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ('username', 'first_name', 'last_name',  'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        
        
        
        