from django import forms
from .models import Pelicula, Genero

class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ['titulo', 'descripcion', 'imagen', 'genero']

class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ['nombre']