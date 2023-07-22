from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#Categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

#Post
class Post(models.Model):
    titulo = models.CharField(max_length=50, null=False)
    subtitulo = models.CharField(max_length=100, null=True, blank=True, default='')
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.TextField(null=False)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, default=None)
    imagen = models.ImageField(null=True, blank=True, upload_to='media', default='static/post_default.png')
    publicado = models.DateTimeField(default=timezone.now)
    
    # Metaclase para definir el orden de los posts en función de la fecha de publicación
    class Meta:
        ordering = ('-publicado',)
        
    def __str__(self):
        return self.titulo
    
    # Método para eliminar un post y su imagen asociada
    def delete(self, using=None, keep_parents=False):
        self.imagen.delete()
        super().delete(using, keep_parents)
    
    # Propiedad que devuelve el total de comentarios asociados a un post
    @property
    def total_comentarios(self):
        return self.comentarios.count()
  
#Perfil        
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    gmail = models.EmailField()

    def __str__(self):
        return self.usuario.username
    
#Colaborador
class Colaborador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    gmail = models.EmailField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.nombre
    
#Comentario
class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario por {self.autor.username} en {self.post.titulo}"
