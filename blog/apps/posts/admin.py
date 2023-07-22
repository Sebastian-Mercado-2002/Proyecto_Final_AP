from django.contrib import admin
from .models import Categoria, Post, Colaborador



class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo', 'categoria')
    list_filter = ('activo', 'categoria')
    actions = ['publicar_posts', 'despublicar_posts']

    def publicar_posts(self, request, queryset):
        queryset.update(activo=True)

    publicar_posts.short_description = "Publicar los posts seleccionados"

    def despublicar_posts(self, request, queryset):
        queryset.update(activo=False)

    despublicar_posts.short_description = "Despublicar los posts seleccionados"


admin.site.register(Post, PostAdmin)
admin.site.register(Categoria)

