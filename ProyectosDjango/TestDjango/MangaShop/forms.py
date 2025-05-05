from django import forms
from .models import Manga, Usuario
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
import re

class MangaForm(forms.ModelForm):
    class Meta:
        model = Manga
        fields = ['nombre', 'autor', 'anio_publicacion', 'volumenes', 'genero', 'portada', 'stock_disponible']


class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, help_text="Debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un símbolo.")

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'fecha_nacimiento', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if (len(password) < 8 or not re.search(r'[A-Z]', password) or
            not re.search(r'[a-z]', password) or not re.search(r'\d', password) or
            not re.search(r'[^\w\s]', password)):
            raise ValidationError('La contraseña no cumple con los requisitos.')
        return password