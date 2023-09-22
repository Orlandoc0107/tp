# Aqui configuramos lo que deseamos serializar en nuestra API Rest
# Por decirlo de alguna forma vamos a indicarle que datos vamso a usar a la hora de enviarlos a tipo Json.

from rest_framework import serializers
from .models import Tarea
from django.contrib.auth.models import User


# class para Tareas
class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'
        
    read_only_fields = (
        'id',
        'created_at',
        'updated_at'
        )


# Class para Usuario
class UserRegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            #email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user