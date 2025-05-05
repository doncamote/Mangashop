from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from MangaShop.models import Manga
from .serializers import MangaSerializers
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt, datetime

class MangaAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def get(self, request):
        mangas = Manga.objects.all()
        serializer = MangaSerializers(mangas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MangaSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MangaDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def get_object(self, pk):
        return get_object_or_404(Manga, pk=pk)

    def put(self, request, pk):
        manga = self.get_object(pk)
        serializer = MangaSerializers(manga, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        manga = self.get_object(pk)
        manga.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

User = get_user_model()

class RegistroAPIView(APIView):
    def post(self, request):
        data = request.data
        required_fields = ['first_name', 'last_name', 'email', 'password', 'password2', 'fecha_nacimiento']
        
        # Validar campos obligatorios
        for field in required_fields:
            if field not in data:
                return Response({"error": f"Falta el campo {field}"}, status=400)

        if data['password'] != data['password2']:
            return Response({"error": "Las contraseñas no coinciden"}, status=400)

        if User.objects.filter(email=data['email']).exists():
            return Response({"error": "Ya existe un usuario con ese correo"}, status=400)

        user = User.objects.create_user(
            username=data['email'],  # Asumimos que usas el correo como username
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.fecha_nacimiento = data['fecha_nacimiento']
        user.save()

        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({"message": "Registro exitoso", "access_token": token}, status=201)