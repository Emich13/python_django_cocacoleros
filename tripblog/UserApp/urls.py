from django.urls import path, include
from UserApp import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('sobreNosotros', views.mantencion, name="nosotros"),
    path('login', views.Login, name="inicioSesion"),
    path('registro', views.register, name="registro"),
    path('logout', LogoutView.as_view(next_page="inicioSesion"), name="Logout"),
    path('perfil', views.verPerfil, name="Perfil"),
    path('editarPerfil', views.editarUsuario, name="editarPerfil"),
    path('otroPerfil/<id>',views.otroPerfil,name="otroPerfil"),
    path('enviarSolicitud/<id>', views.enviarSolicitud, name= "enviarSolicitud"),
    path('aceptarSolicitud/<id>', views.aceptarSolicitud, name= "aceptarSolicitud"),
    path('rechazarSolicitud/<id>', views.rechazarSolicitud, name= "rechazarSolicitud"),
    path('amigos', views.verAmigos, name="amigos"),
    path('eliminarAmigo/<id>',views.eliminarAmigo, name="eliminarAmigo"),
    path('mensajes', views.verMensajes, name="misMensajes"),  
    path('enviarMensaje/<id>',views.enviarMensaje, name="enviarMensaje"),
    path('crearMensaje', views.crearMensaje, name="crearMensaje"),
    path('crearMensaje2', views.crearMensaje2, name="crearMensaje2"),
    path('buscarMensaje', views.buscarMensaje, name="buscarMensaje"),
    path('verMensajeEspecifico/<id>',views.verMensajeEspecifico, name="verMensajeEspecifico"),
    path('verMensajesEnviados', views.verMensajesEnviados, name="verMensajesEnviados"),
    path('eliminarMensaje/<id>', views.eliminarMensaje, name="eliminarMensaje"),
    path('Posteos/<id>', views.verPosteos, name="Posteos"),
    path('comentarios', views.verComentarios, name="comentarios"),
    path('busquedaPost/', views.busquedaPost, name="busquedaPost"),
    path('buscar/', views.buscar), 
    path('eliminarComentario/<id_comentario>',views.eliminarComentario, name="eliminarComentario"),
    path('editarComentario/<id_comentario>/', views.editarComentario, name="editarComentario"),
    path('likes/<id>', views.darLike, name="Likes"),
    path('misLikes', views.verLikes, name="verLikes"),
    path('guardados/<id>', views.postFavoritos, name="Postfavoritos"),
    path('misPostsGuardados', views.verPostFavoritos, name="verPostFavoritos"),
    path('crearPost',views.CrearPost, name ="crearPost"),
    path('listaPost', views.listaPost.as_view(), name='listaPost'),
    path('actualizaPost/<pk>/', views.actualizaPost.as_view(), name='actualizaPost'),
    path('eliminaPost/<pk>/', views.eliminaPost.as_view(), name='eliminaPost'),
    path('Tematicas', views.verTematicas, name="tematicas"),
    path('tematicasList', views.TematicaList.as_view(), name="tematicasList"),
    path('tematicasDetail/<pk>',views.TematicaDetail.as_view(), name="tematicasDetail"),
    path('tematicasDelete/<pk>',views.TematicaDelete.as_view(), name="tematicasDelete"),
    path('tematicasCreate',views.TematicaCreate.as_view(), name="tematicasCreate"),
    path('postRelacionados/<pk>', views.postRelacionados, name="postRelacionados"),
    path('crearTematica',views.CrearTematica, name="crearTematica"),
    path('buscarTematicas', views.buscarTematicas, name="buscarTematicas"),
    path('editarTematicas/<id_tematica>',views.editarTematicas, name= 'editarTematicas'),
    
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    
]

