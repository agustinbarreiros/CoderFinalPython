from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Mensaje, Blog

class RegistroForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PerfilForm(forms.ModelForm):
    imagen = forms.ImageField(required=False)  # Agrega required=False para permitir imágenes opcionales

    class Meta:
        model = Perfil
        fields = ['imagen', 'descripcion']


class MensajeForm(forms.ModelForm):
    destinatario = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Mensaje
        fields = ['destinatario', 'contenido']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['titulo', 'subtitulo', 'cuerpo', 'imagen']
        widgets = {'imagen': forms.ClearableFileInput()}        