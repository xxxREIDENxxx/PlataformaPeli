from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test  
from .models import  Genero, Pelicula, Visualizacion
from .forms import PeliculaForm, GeneroForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse 
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = False

def form_valid(self, form):
        # Redirige al dashboard correspondiente
        if self.request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('dashboard')


def dispatch(self, request, *args, **kwargs):
        # Si el usuario está autenticado y es administrador, redirige al dashboard de admin
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        # Si no está autenticado, procede al formulario de login
        return super().dispatch(request, *args, **kwargs)

@login_required
def dashboard(request):
    if request.user.is_superuser:
        message = "Bienvenido, Administrador."
    else:
        message = "Bienvenido, Usuario."
    return render(request, 'users/dashboard.html', {'message': message})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def get_success_url(self):
    # Si el usuario es administrador, redirige al dashboard de administrador
    if self.request.user.is_superuser:
        return reverse_lazy('admin_dashboard')
    # Si es un usuario normal, redirige al dashboard estándar
    return reverse_lazy('dashboard')

def es_admin(user):
    return user.is_superuser or user.is_staff

# Vista para agregar una película
@login_required
@user_passes_test(es_admin)
def agregar_pelicula(request):
    if request.method == 'POST':
        form = PeliculaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('peliculas_listado')
    else:
        form = PeliculaForm()
    return render(request, 'users/agregar_pelicula.html', {'form': form})

# Vista para editar una película
@user_passes_test(es_admin)
def editar_pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    if request.method == 'POST':
        form = PeliculaForm(request.POST, request.FILES, instance=pelicula)
        if form.is_valid():
            form.save()
            return redirect('peliculas_listado')
    else:
        form = PeliculaForm(instance=pelicula)
    return render(request, 'users/editar_pelicula.html', {'form': form, 'pelicula': pelicula})

# Vista para eliminar una película
@user_passes_test(es_admin)
def eliminar_pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    pelicula.delete()
    return redirect('peliculas_listado')

@login_required
# Vista para agregar un género
@user_passes_test(es_admin)
def agregar_genero(request):
    if request.method == 'POST':
        form = GeneroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('peliculas_listado')
    else:
        form = GeneroForm()
    return render(request, 'users/agregar_genero.html', {'form': form})

def peliculas_listado(request):
    peliculas = Pelicula.objects.all().order_by('-visualizaciones')  # Ordenar por popularidad
    return render(request, 'users/peliculas_listado.html', {'peliculas': peliculas})

def peliculas_listado(request):
    # Obtener todos los géneros para el filtro
    generos = Genero.objects.all()
    
    # Obtener los parámetros de búsqueda
    titulo = request.GET.get('titulo', '')
    genero_id = request.GET.get('genero', '')

    # Filtrar las películas por título y género, y ordenar por popularidad (visualizaciones)
    peliculas = Pelicula.objects.all()
    if titulo:
        peliculas = peliculas.filter(titulo__icontains=titulo)
    if genero_id:
        peliculas = peliculas.filter(genero_id=genero_id)

    peliculas = peliculas.order_by('-visualizaciones')
    
    return render(request, 'users/peliculas_listado.html', {
        'peliculas': peliculas,
        'generos': generos,
        'titulo': titulo,
        'genero_id': genero_id,
    })

def registrar_visualizacion(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    
    # Comprueba si el usuario ha visto la película antes
    if not Visualizacion.objects.filter(usuario=request.user, pelicula=pelicula).exists():
        Visualizacion.objects.create(usuario=request.user, pelicula=pelicula)
        # Aumenta el contador de visualizaciones
        pelicula.visualizaciones += 1
        pelicula.save()

    # Redirige al detalle de la película o a donde prefieras
    return HttpResponseRedirect(reverse('detalle_pelicula', args=[pelicula.id]))

def detalle_pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    return render(request, 'users/detalle_pelicula.html', {'pelicula': pelicula})

@login_required
def marcar_como_vista(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)

    # Verificar si el usuario ya ha marcado la película como vista
    if not Visualizacion.objects.filter(pelicula=pelicula, usuario=request.user).exists():
        # Crear un nuevo registro de visualización
        Visualizacion.objects.create(pelicula=pelicula, usuario=request.user)

        # Incrementar el contador de visualizaciones en el modelo Pelicula
        pelicula.visualizaciones += 1
        pelicula.save()

    # Redirigir al usuario a la página de detalle de la película o a la lista de películas
    return redirect('peliculas_listado')  # Cambia a la URL que prefieras