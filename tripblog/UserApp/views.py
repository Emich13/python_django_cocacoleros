from audioop import reverse
from collections import UserDict
from genericpath import exists
import numbers
from this import d
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from email.policy import default
from django.http import HttpResponse
from urllib import request
from venv import create
from django.contrib.auth.models import User
from dataclasses import fields
from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
import random
from django.views.generic.edit import UpdateView, DeleteView
from UserApp.forms import PostForm,PerfilForm,MensajeForm,TematicaForm, UserRegisterForm, UserEditForm,ComentarioForm, ComentFormulario
from UserApp.models import SolicitudAmistad,MisMensajes , PostFavoritos,Likes,Post,Perfil, Tematica, ComentariosPost
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

def mantencion(req):
    return render(req, 'mantencion.html')

def padre(req):
    return render(req, 'padre.html')

def register(request):

    if request.method == 'POST':
           form = UserRegisterForm(request.POST)
           if form.is_valid():
                print(form.cleaned_data['groups'])
                username = form.cleaned_data['username']
                user = form.save()

                for g in form.cleaned_data['groups']:
                    print(g.name)
                    user.groups.add(g)


                bio = form.cleaned_data['biografia']
                
                Perfil.objects.create(
                    user = user,
                    biografia = form.cleaned_data['biografia']
                )
                
                return render(request,"usuarioCreado.html" ,  {"mensaje":"Usuario Creado :)"})

    else:
            print("No se creo nada")
            form = UserRegisterForm()     

    return render(request,"registro.html" ,  {"form":form})

def Login(request):
    post=Post.objects.all()
    listaTematicas=Tematica.objects.all()

    if request.method == "POST":
            form = AuthenticationForm(request, data = request.POST)

            if form.is_valid():
                  usuario = form.cleaned_data.get('username')
                  contra = form.cleaned_data.get('password')
                  user = authenticate(username=usuario, password=contra)
                  if user is not None:
                    login(request, user) #
                    messages.success(request,'Bienvenido!' )
                    return redirect(inicio)
                  else:
                    return render(request, "loginError.html",{'mensaje': "Error! Datos erróneos"})

            else:
                return render(request, "loginError.html",{'mensaje': "Error! Datos erróneos"})
    form = AuthenticationForm()
    return render(request,"login.html", {'form':form} )

def eliminarCuenta(req):
    pass

def verPerfil(req):
    usuario = req.user
    perfil = Perfil.objects.filter(user=usuario)
    post= Post.objects.filter(posteador=usuario)

    username= usuario.username
    userBio= usuario.perfil.biografia
    email= usuario.email
    avatar= usuario.perfil.imagenPerfil
    print(username)
    print(post)

    return render(req, "perfil.html", {'username':username,'email':email,'biografia':userBio, 'usuario':usuario,'post':post})


def iniciarChat(req):
    return render(req, 'chat.html')

def otroPerfil(req, id):
    otroUser = User.objects.get(id=id)
    postsDelOtroUser= Post.objects.filter(posteador=otroUser)
    print(otroUser)
    print(postsDelOtroUser)
    perfil = Perfil.objects.get(user=otroUser)
    
    return render(req,'otroPerfil.html', {'otroUser': otroUser,'perfil':perfil, 'posts': postsDelOtroUser})

def verAmigos(req):
    perfil = Perfil.objects.get(user=req.user)
    amigos = perfil.amigos
    solicitudes = SolicitudAmistad.objects.filter(to_user=req.user)
    print(amigos)
    return render(req, 'amigos.html', {'amigos':amigos, 'solicitudes':solicitudes})

def eliminarAmigo(req, id):
    otroUser = User.objects.get(id=id)
    user= req.user
    user.perfil.amigos.remove(otroUser)
    otroUser.perfil.amigos.remove(user)
    return redirect(inicio)

def enviarSolicitud(req, id):
    from_user = req.user
    to_user = User.objects.get(id=id)
    SolicitudAmistad.objects.get_or_create(from_user= from_user, to_user = to_user)
    return HttpResponse('solicitud enviada')

def aceptarSolicitud(req, id):
    solicitudAmistad = SolicitudAmistad.objects.get(id= id)
    to_user = req.user
    from_user = solicitudAmistad.from_user
    perfil_to_user=Perfil.objects.get(user = to_user )
    perfil_from_user= Perfil.objects.get( user = from_user)
    
    if solicitudAmistad.to_user == req.user:
        solicitudAmistad.to_user.perfil.amigos.add(solicitudAmistad.from_user)
        solicitudAmistad.from_user.perfil.amigos.add(solicitudAmistad.to_user)
        solicitudAmistad.delete()
        return HttpResponse('solicitud de amistad aceptada')
   
def rechazarSolicitud(req, id):
    solicitudAmistad = SolicitudAmistad.objects.get(id= id)
    solicitudAmistad.delete()
    return HttpResponse('solicitud de amistad eliminada')

def enviarMensaje(req,id):
    destinatario = User.objects.get(id=id)
    if req.method == "POST":
        miForm=MensajeForm(req.POST)
        if miForm.is_valid:
            mensaje=miForm.save(commit=False)
            mensaje.user=req.user
            mensaje.destinatario= destinatario
            mensaje.save()
            miForm.save_m2m()
            return redirect(inicio)
        else:
            return HttpResponse('Los datos ingresados son incorrectos')
    else:
        miForm= MensajeForm()
    return render(req, 'crearMensaje.html',{'miForm':miForm,'destinatario':destinatario})

def crearMensaje(req): 
    return render(req, 'crearMensaje2.html')

def crearMensaje2(req):
    destino = req.POST['destinatario']
    mensaje = req.POST['mensaje']
    if User.objects.filter(username=destino).exists():
        destinoFinal = User.objects.get(username=destino)
        MisMensajes.objects.create(user=req.user, mensaje=mensaje, destinatario=destinoFinal)
        return HttpResponse("mensaje enviado!")
    else:
        return HttpResponse('el usuario destino no existe!')
    
def verMensajes(req):
    
    destinatario = req.user
    mensaje = MisMensajes.objects.filter(destinatario=destinatario)
    return render(req, 'mensajesDirectos.html', {
        'mensaje':mensaje
        
    })

def verMensajesEnviados(req):
    mensajes= MisMensajes.objects.filter(user=req.user)
    return render(req, 'mensajesEnviados.html', {'mensajes':mensajes})

def verMensajeEspecifico(req,id):
    mensajeEsp = MisMensajes.objects.get(id=id)
    return render(req, 'mensajeEspecifico.html', {'mensajeEsp':mensajeEsp})

def eliminarMensaje(req,id):
    mensajeEliminar = MisMensajes.objects.get(id=id)
   
    mensajeEliminar.delete()
    return redirect(inicio)

def buscarMensaje(req):
    if req.GET['usuario']:
        usuario     = req.GET['usuario']
        
        if User.objects.filter(username=usuario).exists():
            u=User.objects.get(username=usuario)
            mensajesRecibidos = MisMensajes.objects.filter(user=u)
            mensajesEnviados = MisMensajes.objects.filter(destinatario=u)
            return render(req, 'mensajesBuscados.html', {'mensajesRecibidos':mensajesRecibidos,'mensajesEnviados':mensajesEnviados} )
        else:
            mensajeError=f'No se encontraron mensajes asociados a {usuario}!'
            return render(req,'mensajesBuscados.html',{'mensajeError':mensajeError})

    else:
        respuesta = "No hay datos"
        return render(req, 'mensajesBuscados.html',{'respuesta':respuesta} )

def editarUsuario(req):
    usuario = req.user
    perfil = req.user.perfil
    if req.method == 'POST':
        miForm = UserEditForm(req.POST, instance = usuario)
        miPerfil= PerfilForm(req.POST, req.FILES, instance=perfil)
        if miForm.is_valid() and miPerfil.is_valid():
            info= miForm.cleaned_data
            perfil1 = miPerfil.cleaned_data
            usuario.email = info['email']
            usuario.first_name= info['first_name']
            usuario.last_name= info['last_name']
            new_password = info['password1']
            usuario.set_password(new_password)
            perfil.imagenPerfil= perfil1['imagenPerfil'] 
            perfil.biografia = perfil1['biografia']
            miPerfil.save()
            usuario.save()
            return redirect(inicio)
    else:
        miForm = UserEditForm(initial={'email': usuario.email,'first_name':usuario.first_name ,'last_name': usuario.last_name,'password':usuario.password})
        miPerfil = PerfilForm(instance=perfil)
        return render(req, 'editarPerfil.html',{'miForm':miForm, 'miPerfil': miPerfil,'usuario':usuario})

def mensajes(req):
    return render(req,'mensajesDirectos.html')

def idPost(id):
    return Post.objects.get(id=id)

 
def inicio(request):
    post=Post.objects.all()
    listaTematicas=Tematica.objects.all() 
    page=request.GET.get('page',1)
    paginator = Paginator(post,4)
  
    try:
        posteos=paginator.page(page)
    except PageNotAnInteger:
        posteos=paginator.page(1)
    except EmptyPage:
        posteos= paginator.page(paginator.num_pages)
    contexto={
        'post':post,
        'lista': listaTematicas,
        'posteos':posteos
      
    }

    
    if not request.user.is_authenticated:
        return render(request, 'inicio.html', contexto)
    else:
        return render(request, 'inicio.html', contexto)

def verPosteos(req,id):
    post=Post.objects.get(id=id)
    comentario= ComentariosPost.objects.filter(post__id=id)
    tematicas=Tematica.objects.filter(post__id=id) 
    lista= Tematica.objects.all()

    if req.method=="POST":
        miFormComentario=ComentarioForm(req.POST)
        if req.user.is_authenticated:
            if miFormComentario.is_valid:
                comentarioNuevo= miFormComentario.save(commit=False)
                comentarioNuevo.comentarista= req.user
                comentarioNuevo.post=post
                comentarioNuevo.save()
            else:
                return HttpResponse("Error, comentario no enviado :( envienos un mensaje en la sección sobre nosotros")
        else:
            return HttpResponse("Necesitar iniciar sesión para comentar!")
    else:
        miFormComentario=ComentarioForm()
    return render(req,'posteos.html', {'post':post, 'tematicas':tematicas, 'comentario':comentario, 'miFormComentario': miFormComentario, 'lista':lista})

@login_required
def darLike(req,id):
    post = get_object_or_404(Post, id=id)
    likes = Likes.objects.filter(usuario=req.user, post=post)
    if likes.exists():
        likes.delete()
        return redirect('Posteos',id=id)
    Likes.objects.create(usuario=req.user, post=post)
    return redirect('Posteos',id=id)

def verLikes(req):
    likes = Likes.objects.filter(usuario=req.user)
    
    return render(req, "misLikes.html", {'likes':likes})
@login_required
def postFavoritos(req, id):
    post= get_object_or_404(Post, id=id)
    postFav= PostFavoritos.objects.filter(user=req.user, post=post)
    if postFav.exists():
        postFav.delete()
        return redirect('Posteos', id=id)
    PostFavoritos.objects.create(user=req.user,post=post)
    return redirect('Posteos',id=id)

def verPostFavoritos(req):
    postFav= PostFavoritos.objects.filter(user=req.user)
    return render(req, 'misPostGuardados.html',{'postFav':postFav})

@login_required
def CrearPost(req):

    if req.method == "POST":
        miForm=PostForm(req.POST, req.FILES)
        if miForm.is_valid:
            post=miForm.save(commit=False)
            post.posteador=req.user
            post.save()
            miForm.save_m2m()
            return redirect(inicio)
        else:
            return HttpResponse('Los datos ingresados son incorrectos')
    else:
        miForm= PostForm()
    return render(req, 'crearPost.html',{'miForm':miForm})

def busquedaPost(req):
    return render(req, "UserApp/busquedaPost.html")

def buscar(request):
    if request.GET['titulo']:
        titulo=request.GET['titulo']
        if Post.objects.filter(titulo=titulo).exists():
            post = Post.objects.filter(titulo__icontains=titulo)
            return render(request, 'UserApp/resultadosBusqueda.html', {"post": post, "titulo":titulo })
        else:
            mensajeError = f'No se encontraron post con el titulo {titulo}!'
            return render(request, 'UserApp/resultadosBusqueda.html',{'mensajeError':mensajeError} )
    else:
        respuesta = "No hay datos"
        return render(request, 'UserApp/resultadosBusqueda.html',{'respuesta':respuesta} )

def verTematicas(req):
    listaTematicas= Tematica.objects.all()
    return render(req,'tematicas.html',{"listaTematicas": listaTematicas})

class TematicaCreate(CreateView):
    model=Tematica

class TematicaList(ListView):
    model= Tematica
    template_name= "tematicas_List.html"

class TematicaDetail(DetailView):
    model= Tematica
    template_name="tematicas_detalle.html"

class TematicaUpdate(UpdateView):
    model=Tematica
    success_url= 'UserApp/tematicasList'
    fields= ['nombre']

class TematicaDelete(DeleteView):
    model= Tematica
    success_url=  reverse_lazy('tematicasList') 
    template_name= "tematica_delete.html"

def postRelacionados(req, pk):
    
    post= Post.objects.filter(tematica__id=pk)

    return render(req,'postRelacionados.html', {'postRelacionados' : post})

def CrearTematica(req):

    if req.method== 'POST':
        miForm=TematicaForm(req.POST)
        if miForm.is_valid:
            miForm.save()
            return redirect(inicio)
        else:
            return HttpResponse('Los datos ingresados son incorrectos')
    else:
        miForm=TematicaForm()
    
    return render(req, 'crearTematica.html',{'miForm': miForm})

def buscarTematicas(req):
    if req.GET['tematica']:
        tematica=req.GET['tematica']
        nombreTematica=Tematica.objects.filter(nombre__icontains=tematica)
        return render(req, "resultados.html", {'tematicas':nombreTematica})
    else:
        respuesta="No enviaste datos"
    return HttpResponse(respuesta)

def eliminarTematicas(req, id_tematica):
    tematica= Tematica.objects.get(id=id_tematica)
    tematica.delete()
    listaTematicas= Tematica.objects.all()
    return render(req, 'tematicas.html',{'listaTematicas': listaTematicas})

def editarTematicas(req, id_tematica):
    tematica= Tematica.objects.get(id=id_tematica)
    listaTematicas= Tematica.objects.all()
    if req.method=='POST':
        miForm= TematicaForm(req.POST)
        if miForm.is_valid:
            info=miForm.cleaned_data
            tematica.nombre= info['nombre']
            tematica.save()
            return render(req, 'tematicas.html',{'listaTematicas': listaTematicas}) 
    else:
        miForm= TematicaForm(initial={'nombre':tematica.nombre})
    return render(req, 'editarTematicas.html',{'miForm':miForm})

def verComentarios(req):
    comentario= ComentariosPost.objects.filter(comentarista=req.user)
   
    return render(req, 'comentarios.html', {'comentario':comentario})

def eliminarComentario(req, id_comentario):
    comentario= ComentariosPost.objects.get(id=id_comentario)
    comentario.delete()
    comentarioCompleto= ComentariosPost.objects.filter(comentarista=req.user) 
    return render(req, 'comentarios.html', {'comentario':comentarioCompleto})

def editarComentario(req, id_comentario):
    comentario = ComentariosPost.objects.get(id=id_comentario)
    if req.method=="POST":

        miFormComentario = ComentarioForm(req.POST) 
        print(miFormComentario)
        if miFormComentario.is_valid:
            informacion                     = miFormComentario.cleaned_data
            comentario.contenido_comentario = informacion['contenido_comentario']
            comentario.save()
        else:
            return HttpResponse("No funcionaaaaaaa")

    else: 
        miFormComentario= ComentarioForm(initial={'contenido_comentario': comentario.contenido_comentario}) 
        
    return render(req, "editarComentario.html", {"miFormulario":miFormComentario, "id_comentario":id_comentario})
    
# @login_required
# def leerposts(req):
#     post = Post.objects.all()
#     contexto = {"post": post}

#     return render(req, 'buscar_post.html', contexto)

class listaPost(LoginRequiredMixin,ListView):
    model = Post
    template_name = "buscar_post.html"
    def get_context_data(self,*args, **kwargs):
        context = super(listaPost, self).get_context_data(*args,**kwargs)
        context['posts'] = Post.objects.filter(posteador=self.request.user)
        return context
    
class detallePost(DetailView):
    model = Post
    template_name = "detalle_post.html"

class actualizaPost(UpdateView):
    model = Post
    success_url = "/UserApp/listaPost"
    fields = ["titulo","subtitulo", "contenido", "tematica", "imagenPost"]
    success_message = 'Post editado!'

class postCreate(CreateView):
    model = Post
    fields = ["posteador", "titulo", "subtitulo", "contenido", "fecha_publicacion", "tematica", "estado", "imagenPost"]
    success_url = '/UserApp/listaPost'

class eliminaPost(DeleteView):
    model = Post
    success_url = '/UserApp/listaPost'
    template_name = 'post_confirm_delete.html'