import jwt
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import json
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer



@csrf_exempt
def login_jwt_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            payload = {
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            print(f"Generated Token: {token}")             
            return JsonResponse({'access_token': token})
        else:
            return JsonResponse({'error': 'Credenciales inválidas'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def pagina_protegida(request):
    return render(request, 'mangas/pagina_protegida.html')


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario registrado correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)