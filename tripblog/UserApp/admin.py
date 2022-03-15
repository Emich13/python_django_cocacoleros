from django.contrib import admin
from UserApp.models import Perfil,MisMensajes,SolicitudAmistad,ComentariosPost, Likes, Post, Tematica, PostFavoritos

admin.site.register(Tematica)


admin.site.register(Post)

admin.site.register(ComentariosPost)

admin.site.register(Likes)


admin.site.register(Perfil)

admin.site.register(PostFavoritos)

admin.site.register(MisMensajes)



admin.site.register(SolicitudAmistad)