
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def _str_(self):
        return self.nombre
    
class Pelicula(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='peliculas/', blank=True, null=True)
    genero = models.ForeignKey('Genero', on_delete=models.CASCADE, related_name="peliculas")
    visualizaciones = models.PositiveIntegerField(default=0)

    def _str_(self):
        return self.titulo

class Visualizacion(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='visualizaciones_usuario')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_visualizacion = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.usuario.username} - {self.pelicula.titulo}"

class Meta:
    unique_together = ('usuario', 'pelicula')