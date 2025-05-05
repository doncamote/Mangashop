from django.urls import path
from . import views
from MangaShop.views import lista_manga
from .views import MangaAPIView, MangaDetailAPIView, RegistroAPIView

urlpatterns = [
    path('MangaShop/', lista_manga, name='lista_manga'),    path('mangas/', MangaAPIView.as_view(), name='manga-list-create'),
    path('mangas/<int:pk>/', MangaDetailAPIView.as_view(), name='manga-detail'),
    path('registro/', RegistroAPIView.as_view(), name='registro_api'),
]
