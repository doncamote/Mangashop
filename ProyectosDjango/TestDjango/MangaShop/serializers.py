from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from .models import Usuario



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            validate_password,
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])',
                message='La contraseña debe contener al menos una mayúscula, una minúscula, un número y un carácter especial.'
            )
        ]
    )

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'fecha_nacimiento', 'password')

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value

    def create(self, validated_data):
        user = Usuario(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            fecha_nacimiento=validated_data['fecha_nacimiento'],
            username=validated_data['email']  # Si decides ocultar el campo username
        )
        user.set_password(validated_data['password'])
        user.save()
        return user