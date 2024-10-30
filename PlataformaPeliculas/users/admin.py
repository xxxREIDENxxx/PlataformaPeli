
# Register your models here.
from django.contrib import admin
from .models import Pelicula, Genero

# Registrar los modelos en el panel de administración
admin.site.register(Pelicula)
admin.site.register(Genero)