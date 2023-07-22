from django import forms
from apps.posts.models import Post, Colaborador, Comentario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Formulario para crear y editar un Post
class PostForm(forms.ModelForm):
    eliminar_imagen = forms.BooleanField(required=False)

    class Meta:
        model = Post
        fields = ('titulo', 'subtitulo', 'texto', 'categoria', 'imagen', 'eliminar_imagen')
        
# Formulario para registrar un nuevo usuario
class RegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=30)
    gmail = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'nombre', 'gmail', 'password1', 'password2', 'bio')
        
# Formulario para iniciar sesión (login)
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password'].label = 'Contraseña'
        
# Formulario para registrar un nuevo Colaborador
class ColaboradorRegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=100)
    gmail = forms.EmailField(max_length=100)
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'nombre', 'gmail', 'bio')
        
# Formulario para editar el perfil de un Colaborador
class ColaboradorPerfilForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ('nombre', 'gmail', 'bio')

# Formulario para agregar un Comentario
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('contenido',)
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 4}),
        }
