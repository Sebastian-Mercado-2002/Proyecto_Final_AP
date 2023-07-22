from django.contrib import admin
from . import views
from django.urls import path
from .views import index, aplicacion_de_la_ia, impacto_educacion, impacto_laboral, acerca_de, editar_articulo, editar_imagen, eliminar_articulo
from .views import contacto, inicio, crear_post, registro, CustomLoginView, cuenta, registrar_colaborador, listar_colaboradores
from .views import agregar_comentario, editar_comentario, eliminar_comentario
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from .forms import PostForm, RegistroForm, ColaboradorRegistroForm, ColaboradorPerfilForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('aplicacion_de_la_ia/', aplicacion_de_la_ia, name='aplicacion_de_la_ia'),
    path('impacto_educacion/', impacto_educacion, name='impacto_educacion'),
    path('impacto_laboral/', impacto_laboral, name='impacto_laboral'),
    path('acerca_de/', acerca_de, name='acerca_de'),
    path('contacto/', contacto, name='contacto'),
    path('inicio/', inicio, name='inicio'),
    path('crear/', crear_post, name='crear_post'),
    path('editar_articulo/<int:pk>/', editar_articulo, name='editar_articulo'),
    path('eliminar_articulo/<int:pk>/', eliminar_articulo, name='eliminar_articulo'),
    path('editar_imagen/<int:pk>/', editar_imagen, name='editar_imagen'),
    path('registro/', registro, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('cuenta/', cuenta, name='cuenta'),
    path('accounts/profile/', RedirectView.as_view(pattern_name='index'), name='profile'),
    path('registro_colaborador/', registrar_colaborador, name='registro_colaborador'),
    path('colaboradores/', listar_colaboradores, name='colaboradores'),
    path('agregar_comentario/<int:pk>/', agregar_comentario, name='agregar_comentario'),
    path('editar_comentario/<int:pk>/', editar_comentario, name='editar_comentario'),
    path('eliminar_comentario/<int:pk>/', eliminar_comentario, name='eliminar_comentario'),
    path('detalle_post/<int:pk>/', views.detalle_post, name='detalle_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
