import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Manga, Usuario
from .forms import MangaForm
from django.contrib import messages
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserRegisterSerializer
from django.views.decorators.csrf import csrf_exempt
from MangaShop.models import Manga
from api_rest.serializers import MangaSerializers
from .decorators import jwt_login_required
from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse
import jwt
from django.conf import settings
import datetime
from django.contrib.auth.backends import ModelBackend



@api_view(['GET', 'POST'])
def lista_manga(request):
    if request.method == 'GET':
        mangas = Manga.objects.all()
        serializer = MangaSerializers(mangas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MangaSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def pagina_inicio(request):
    return render(request, 'mangas/home.html')

def home(request):
    mangas = Manga.objects.all()  
    return render(request, 'mangas/lista.html', {'mangas': mangas})

def agregar_manga(request):
    if request.method == 'POST':
        form = MangaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalogo_mangas')  
    else:
        form = MangaForm()
    return render(request, 'mangas/formulario.html', {'form': form})

def editar_manga(request, id):
    manga = get_object_or_404(Manga, id=id)
    if request.method == 'POST':
        form = MangaForm(request.POST, request.FILES, instance=manga)
        if form.is_valid():
            form.save()
            return redirect('catalogo_mangas')  
    else:
        form = MangaForm(instance=manga)
    return render(request, 'mangas/formulario.html', {'form': form})

def eliminar_manga(request, id):
    manga = get_object_or_404(Manga, id=id)
    if request.method == 'POST':
        manga.delete()
        return redirect('catalogo_mangas')  
    return render(request, 'mangas/confirmar_eliminacion.html', {'manga': manga})


@jwt_login_required
def pagina_protegida(request):
    return render(request, 'mangas/pagina_protegida.html')

def login_view(request):
    return render(request, 'mangas/login.html')


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            })
        return Response({'detail': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED) 

class RegistroUsuarioAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Usuario registrado exitosamente."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PaginaProtegidaAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "mensaje": f"Bienvenido {user.first_name} {user.last_name}, estás autenticado.",
            "email": user.email
        })

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username or kwargs.get('email')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

def mangas_extras(request):
    # 1. Jikan API - búsqueda de manga
    jikan_url = "https://api.jikan.moe/v4/manga?q=dr%20stone"
    jikan_data = []
    try:
        jikan_response = requests.get(jikan_url, timeout=5)
        if jikan_response.status_code == 200:
            jikan_data = jikan_response.json().get("data", [])[:3]  # Solo 3 resultados
    except requests.exceptions.RequestException:
        jikan_data = []

    # 2. Animechan API - frase aleatoria
    kitagawachan_url = "https://kitagawachan-api.vercel.app/quotes/random"
    anime_quote = {}
    try:
        response = requests.get(kitagawachan_url, timeout=5)
        if response.status_code == 200:
            anime_quote = response.json()
        else:
            anime_quote = {
                "anime": "N/A",
                "character": "N/A",
                "quote": "No se pudo obtener la frase."
            }
    except requests.exceptions.RequestException:
        anime_quote = {
            "anime": "N/A",
            "character": "N/A",
            "quote": "No se pudo obtener la frase."
        }

    return render(request, "mangas/extras.html", {
        "jikan_mangas": jikan_data,
        "anime_quote": anime_quote
    })