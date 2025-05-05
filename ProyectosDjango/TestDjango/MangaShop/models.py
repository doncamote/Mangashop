from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.utils import timezone


class Manga(models.Model):
    TIPO_GENERO = [
        ('Accion', 'Acción'),
        ('Aventura', 'Aventura'),
        ('Comedia', 'Comedia'),
        ('Drama', 'Drama'),
        ('Romantico', 'Romántico'),
        ('Fantasia', 'Fantasía'),
        ('Ciencia Ficcion', 'Ciencia Ficción'),
        ('Horror', 'Horror'),
        ('Misterio', 'Misterio'),
        ('Supervivencia', 'Supervivencia'),
        ('Slice of Life', 'Slice of Life'),
        # Puedes agregar más géneros según tu catálogo
    ]
    
    # Información básica del manga
    nombre = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    anio_publicacion = models.PositiveIntegerField()  # Año de publicación (sin ñ)
    volumenes = models.PositiveIntegerField()  # Número de volúmenes (sin tilde)
    genero = models.CharField(max_length=50, choices=TIPO_GENERO, default='Accion')
    portada = models.ImageField(upload_to='mangas/portadas/', blank=True, null=True)
    stock_disponible = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class UsuarioManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, fecha_nacimiento, password=None):
        if not email:
            raise ValueError("El email es obligatorio.")
        email = self.normalize_email(email)
        usuario = self.model(email=email, first_name=first_name, last_name=last_name, fecha_nacimiento=fecha_nacimiento)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, first_name, last_name, fecha_nacimiento, password):
        usuario = self.create_user(email, first_name, last_name, fecha_nacimiento, password)
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'  # El campo que se usará para iniciar sesión
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'fecha_nacimiento']
    
    objects = UsuarioManager()
    
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = "mangashop_usuario" 