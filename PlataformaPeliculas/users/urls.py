from django.urls import path
from .views import CustomLoginView, dashboard, register, agregar_pelicula, agregar_genero, peliculas_listado, registrar_visualizacion, detalle_pelicula, marcar_como_vista, peliculas_listado
from django.contrib.auth.views import LogoutView
from django.conf import settings
from . import views
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('admin_dashboard/', dashboard, name='admin_dashboard'),
    path('agregar_pelicula/', agregar_pelicula, name='agregar_pelicula'),
    path('agregar_genero/', agregar_genero, name='agregar_genero'),
    path('peliculas/', peliculas_listado, name='peliculas_listado'),
    path('pelicula/<int:pelicula_id>/ver/', registrar_visualizacion, name='registrar_visualizacion'),
    path('pelicula/<int:pelicula_id>/', detalle_pelicula, name='detalle_pelicula'),
    path('pelicula/<int:pelicula_id>/vista/', views.marcar_como_vista, name='marcar_como_vista'),
    path('peliculas/', views.peliculas_listado, name='peliculas_listado'),
    path('agregar_pelicula/', views.agregar_pelicula, name='agregar_pelicula'),
    path('editar_pelicula/<int:pelicula_id>/', views.editar_pelicula, name='editar_pelicula'),
    path('eliminar_pelicula/<int:pelicula_id>/', views.eliminar_pelicula, name='eliminar_pelicula'),
    path('agregar_genero/', views.agregar_genero, name='agregar_genero'),
]

   
   