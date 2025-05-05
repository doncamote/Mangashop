from django.urls import path, include
from . import views
from MangaShop import views
from .viewsLogin import login_jwt_view, RegisterView
from .views import pagina_protegida, PaginaProtegidaAPI
from . import viewsLogin
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.pagina_inicio, name='inicio'),    
    path('catalogo/', views.home, name='catalogo_mangas'),  
    path('agregar/', views.agregar_manga, name='agregar'),  
    path('editar/<int:id>/', views.editar_manga, name='editar'),  
    path('eliminar/<int:id>/', views.eliminar_manga, name='eliminar'),  
    path('login/', views.login_view, name='mostrar_login'),    
    path('api/login/', viewsLogin.login_jwt_view, name='api_login'),
    path('api/register/', views.RegistroUsuarioAPIView.as_view(), name='api_register'), 
    path('pagina-protegida/', viewsLogin.pagina_protegida, name='pagina_protegida'),
    path('api/pagina-protegida/', PaginaProtegidaAPI.as_view(), name='pagina_protegida_api'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('mangas/extras/', views.mangas_extras, name='mangas_extras'),
    ]
