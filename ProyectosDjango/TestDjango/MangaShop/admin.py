from django.contrib import admin
from .models import Manga, Usuario

admin.site.register(Usuario)

class MangaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'autor', 'año_publicacion', 'genero', 'numero_volumenes', 'stock_disponible')
    search_fields = ('nombre', 'autor', 'genero')
    list_filter = ('genero', 'año_publicacion')

