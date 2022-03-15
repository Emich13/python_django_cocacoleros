import email
from mimetypes import init
from re import S
from UserApp.models import Post, Tematica,MisMensajes,ComentariosPost,Perfil
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class PostFormulario(forms.Form):   
    titulo              = forms.CharField(max_length=100)
    subtitulo           = forms.CharField(max_length=100)
    contenido           = forms.CharField(max_length=100000000)
    tematica            = forms.CharField(max_length=100)
    imagenPost          = forms.ImageField(required=False)

class ComentFormulario(forms.Form):
    contenido_comentario = forms.CharField(max_length=100)

class UserRegisterForm(UserCreationForm):
    email= forms.EmailField()
    password1= forms.CharField(label = 'Contraseña', widget= forms.PasswordInput)
    password2=forms.CharField(label = 'Repetir contraseña', widget= forms.PasswordInput)
    biografia=forms.CharField(label = 'Quien es usted? (opcional)')
    first_name=forms.CharField()
    last_name=forms.CharField()

    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2','first_name','last_name' ,'biografia', 'groups']
        help_texts= {k:"" for k in fields}


class UserEditForm(UserCreationForm):
    email= forms.EmailField()
    password1= forms.CharField(label='Contraseña', widget= forms.PasswordInput)
    password2=forms.CharField(label='Repetir contraseña', widget= forms.PasswordInput)
    first_name= forms.CharField()
    last_name= forms.CharField()
    class Meta:
        model = User
        fields = ['email','password1', 'password2','first_name', 'last_name']
class PerfilForm(forms.ModelForm):
    imagenPerfil= forms.ImageField(required=False, widget=forms.FileInput)
    biografia= forms.CharField()
    class Meta:
        model = Perfil
        fields = ['imagenPerfil', 'biografia']
class PostForm(forms.ModelForm):
    class Meta:  
        model=Post
        fields = ('titulo', 'subtitulo', 'contenido','tematica','imagenPost')
        label={
            'titulo': 'Titulo del posteo',
            'contenido': 'Contenido',
            'tematica':'Tematica',
            'imagenPost': 'Imagen', 
        }
        widgets = {
            'titulo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el titulo del posteo'
                }
            ),
            'subtitulo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el subtitulo del posteo'
                }
            ),
            'contenido': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Desahoguese...'
                }
            ),
            'tematica': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                    
                }
            ),
            'imagenPost': forms.FileInput(
                attrs={
                    'required':False
                }
            )
           
            
            }
 



class TematicaForm(forms.ModelForm):
    class Meta:
        model=Tematica
        fields=('nombre',)
        label={
            'nombre': 'Nombre de la tematica'
        }
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la tematica...'
                }
            )
        }
    

class ComentarioForm(forms.ModelForm):
    class Meta:
        model=ComentariosPost
        fields=('contenido_comentario',)
        label={
            'contenido_comentario': 'Comentario'
        }
        widgets = {
            'contenido_comentario':forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Desahoguese...'
                }
            )
        }

class MensajeForm(forms.ModelForm):
    class Meta:
        model = MisMensajes
        fields=('mensaje',)
        label={
            'mensaje': 'Mensaje'
        }
        widgets = {
            'mensaje':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'placeholder':'Escriba su mensaje aqui'
                }
            )
        }
