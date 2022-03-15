from itertools import count
from django.utils import timezone
from tkinter import CASCADE
from django.db import models
from django.conf import Settings,settings
from django.contrib.auth.models import User
import uuid




class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    imagenPerfil =models.ImageField(upload_to= 'avatares', null=True, default = 'PorDefecto/profileImageDefault.jpg' )
    amigos = models.ManyToManyField(User, blank = True, related_name="Amigos")
    
    biografia = models.TextField(max_length=500, null=True, blank=True)
class SolicitudAmistad(models.Model):
    to_user = models.ForeignKey(User, related_name= "to_user",on_delete=models.CASCADE)
    from_user = models.ForeignKey(User,related_name= "from_user", on_delete=models.CASCADE)
    def __str__(self):
        return f'from: {self.from_user} to: {self.to_user}'

class Tematica(models.Model):
    nombre=models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre}'


class Post(models.Model):
    id= models.AutoField(primary_key=True)
    posteador= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    titulo= models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=100, null= True)
    contenido= models.TextField()
    fecha_publicacion=models.DateTimeField(default=timezone.now)
    
    tematica= models.ManyToManyField(Tematica)
    estado= models.BooleanField('Publicado/NoPublicado', default=True)
    imagenPost= models.ImageField(null=True, blank=True, upload_to = 'imagenes', max_length = 255)
    def __str__(self):
        return f'Posteo:   {self.titulo}, posteador: {self.posteador}'

    def get_tematica(self):
        tematicas= self.tematica.all()
        return tematicas
    def get_comment_count(self):
        return self.comentariospost_set.all().count()
    def get_view_count(self):
        return self.vistadelpost_set.all().count()
    def get_like_count(self):
        return self.likes_set.all().count()

class Likes(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    usuario=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'Like de: {self.usuario}, post= {self.post.titulo}'
class ComentariosPost(models.Model):
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    fecha= models.DateTimeField(default=timezone.now)
    contenido_comentario=models.TextField()
    comentarista= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="comentarista")
    
    def __str__(self):
        return f'Comentario:   {self.contenido_comentario} user: {self.comentarista}'

class PostFavoritos(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f'Fav de: {self.user}, post= {self.post}'
  


class MisMensajes(models.Model):
    user=models.ForeignKey(User,related_name="desde",on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User,related_name="destinatario", on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=200)
    fechaMensaje = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'de: {self.user}, para: {self.destinatario}'


