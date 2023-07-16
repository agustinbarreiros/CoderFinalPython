from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    titulo = models.CharField(max_length=30)
    subtitulo = models.CharField(max_length=30)
    cuerpo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='blog_images/')

    def __str__(self):
        return self.titulo
    

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='perfil_imagenes/', blank=True)
    descripcion = models.TextField(blank=True)
    #pagina_web = models.URLField(blank=True)

    def __str__(self):
        return self.usuario.username 

class Mensaje(models.Model):
    remitente = models.ForeignKey(User, related_name='mensajes_enviados', on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User, related_name='mensajes_recibidos', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De: {self.remitente.username} - Para: {self.destinatario.username}"       