from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .forms import PostForm, RegistroForm, ColaboradorRegistroForm, ColaboradorPerfilForm, ComentarioForm
from apps.posts.models import Post, Categoria, Perfil, Colaborador, Comentario
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden

# Función para comprobar si un usuario es un Colaborador
def is_colaborador(user):
    return user.groups.filter(name='Colaboradores').exists()

def index(request):
    is_colaborador = request.user.groups.filter(name='Colaboradores').exists()
    return render(request, 'index.html', {'is_colaborador': is_colaborador, 'user': request.user})

def aplicacion_de_la_ia(request):
    try:
        categoria = Categoria.objects.get(nombre='Aplicación de la IA')
        posts = Post.objects.filter(categoria=categoria)
    except Categoria.DoesNotExist:
        posts = []
        
    es_colaborador = request.user.groups.filter(name='Colaboradores').exists()
    return render(request, 'aplicacion_de_la_ia.html', {'posts': posts, 'es_colaborador': es_colaborador})

def impacto_educacion(request):
    try:
        categoria = Categoria.objects.get(nombre='Impacto de la IA en educación')
        posts = Post.objects.filter(categoria=categoria)
    except Categoria.DoesNotExist:
        posts = []
        
    es_colaborador = request.user.groups.filter(name='Colaboradores').exists()
    return render(request, 'impacto_educacion.html', {'posts': posts, 'categoria': categoria, 'es_colaborador': es_colaborador})

def impacto_laboral(request):
    try:
        categoria = Categoria.objects.get(nombre='Impacto en el mundo laboral')
        posts = Post.objects.filter(categoria=categoria)
    except Categoria.DoesNotExist:
        posts = []
        
    es_colaborador = request.user.groups.filter(name='Colaboradores').exists()
    return render(request, 'impacto_laboral.html', {'posts': posts, 'categoria': categoria, 'es_colaborador': es_colaborador})


def acerca_de(request):
    return render(request, 'acerca_de.html')

def contacto(request):
    return render(request, 'contacto.html')

def inicio(request):
    return render(request, 'inicio.html')

def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.activo = True
            post.save()
            messages.success(request, '¡El post se ha creado correctamente!')
            return redirect('index')
        else:
            messages.error(request, 'Ha ocurrido un error. Por favor, verifica los campos.')
    else:
        form = PostForm()
    return render(request, 'crear_post.html', {'form': form})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            nombre = form.cleaned_data.get('nombre')
            gmail = form.cleaned_data.get('gmail')
            perfil = Perfil(usuario=user, nombre=nombre, gmail=gmail)
            perfil.save()

            # Obtener el perfil seleccionado en el formulario de registro
            perfil_seleccionado = form.cleaned_data.get('perfil')

            # Asignar usuario al grupo de Colaboradores si es un Colaborador
            if perfil_seleccionado == 'colaborador':
                colaboradores_group = Group.objects.get(name='Colaboradores')
                user.groups.add(colaboradores_group)

            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'register.html', {'form': form})

# Vista para el inicio de sesión personalizado
class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('cuenta')
    
# Vista para la página de cuenta de usuario
@login_required
def cuenta(request):
    colaborador = Colaborador.objects.filter(usuario=request.user).first()
    if request.method == 'POST':
        form = ColaboradorPerfilForm(request.POST, instance=colaborador)
        if form.is_valid():
            colaborador = form.save(commit=False)
            colaborador.usuario = request.user
            colaborador.save()
            return redirect('cuenta')
    else:
        form = ColaboradorPerfilForm(instance=colaborador)
    return render(request, 'cuenta.html', {'form': form, 'colaborador': colaborador})

# Vista para listar todos los colaboradores
def registrar_colaborador(request):
    if request.method == 'POST':
        form = ColaboradorRegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            nombre = form.cleaned_data.get('nombre')
            gmail = form.cleaned_data.get('gmail')
            bio = form.cleaned_data.get('bio')
            colaborador = Colaborador(usuario=user, nombre=nombre, gmail=gmail, bio=bio)
            colaborador.save()

            # Asignar usuario al grupo de Colaboradores
            colaboradores_group = Group.objects.get(name='Colaboradores')
            colaboradores_group.user_set.add(user)

            return redirect('index')
    else:
        form = ColaboradorRegistroForm()
    return render(request, 'registro_colaborador.html', {'form': form})


def listar_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    return render(request, 'colaboradores.html', {'colaboradores': colaboradores})

# Vistas para editar y eliminar artículos (requieren que el usuario sea un Colaborador)
user_passes_test(is_colaborador)
def editar_articulo(request, pk):
    post = get_object_or_404(Post, pk=pk, autor=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            if form.cleaned_data['eliminar_imagen']:
                post.imagen.delete()
            form.save()
            return redirect('index')
    else:
        form = PostForm(instance=post)
    return render(request, 'editar_articulo.html', {'form': form})

@user_passes_test(is_colaborador)
def eliminar_articulo(request, pk):
    post = get_object_or_404(Post, pk=pk, autor=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    return render(request, 'eliminar_articulo.html', {'post': post})

@user_passes_test(is_colaborador)
def editar_imagen(request, pk):
    post = get_object_or_404(Post, pk=pk, autor=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm(instance=post)
    return render(request, 'crear_post.html', {'form': form})

@login_required
def agregar_comentario(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            contenido = form.cleaned_data['contenido']
            Comentario.objects.create(post=post, autor=request.user, contenido=contenido)
            messages.success(request, '¡Comentario agregado correctamente!')
            return redirect('detalle_post', pk=pk)
        else:
            messages.error(request, 'Ha ocurrido un error. Por favor, verifica los campos del formulario.')
    else:
        form = ComentarioForm()
    return render(request, 'detalle_post.html', {'post': post, 'form': form})


# Vista para editar un comentario
@login_required
def editar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    
    # Verificar si el usuario es el autor del comentario o es un colaborador
    if request.user == comentario.autor or request.user.groups.filter(name='Colaboradores').exists():
        if request.method == 'POST':
            form = ComentarioForm(request.POST, instance=comentario)
            if form.is_valid():
                form.save()
                messages.success(request, '¡Comentario editado correctamente!')
                return redirect('detalle_post', pk=comentario.post.pk)
            else:
                messages.error(request, 'Ha ocurrido un error. Por favor, verifica los campos del formulario.')
        else:
            form = ComentarioForm(instance=comentario)
    
        return render(request, 'editar_comentario.html', {'form': form, 'comentario': comentario})
    else:
        return HttpResponseForbidden("No tienes permiso para editar este comentario.")

# Vista para eliminar un comentario
@login_required
@user_passes_test(is_colaborador)
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    
    # Verificar si el usuario es un colaborador
    if request.method == 'POST':
        print(f"Colaborador: {request.user.username}")
        print(f"Comentario Autor: {comentario.autor.username}")
        
        comentario.delete()
        messages.success(request, '¡Comentario eliminado correctamente!')
        return redirect('detalle_post', pk=comentario.post.pk)
    
    return render(request, 'eliminar_comentario.html', {'comentario': comentario})

def detalle_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            contenido = form.cleaned_data['contenido']
            Comentario.objects.create(post=post, autor=request.user, contenido=contenido)
            return redirect('detalle_post', pk=pk)
    else:
        form = ComentarioForm()
    return render(request, 'detalle_post.html', {'post': post, 'form': form})
