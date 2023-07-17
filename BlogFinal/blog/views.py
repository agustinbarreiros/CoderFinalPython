from django.shortcuts import render,redirect,get_object_or_404
from .models import Blog, Mensaje, Perfil
from .forms import RegistroForm, PerfilForm, MensajeForm, BlogForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages


def inicio(request):
     return render(request, 'blog/inicio.html')


def acerca_de(request):
    return render(request, 'blog/acerca_de.html')

def listar_blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/listar_blogs.html', {'blogs': blogs})

def detalle_pagina(request, page_id):
    pagina = Blog.objects.get(id=page_id)
    return render(request, 'blog/detalle_pagina.html', {'pagina': pagina})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario
            perfil = Perfil(usuario=user)  # Crea un perfil y vincúlalo al usuario
            perfil.save()  # Guarda el perfil
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'blog/registro.html', {'form': form})


@login_required
def perfil(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        perfil = Perfil(usuario=request.user)
        perfil.save()

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)
    
    return render(request, 'blog/perfil.html', {'form': form})

@login_required
def enviar_mensaje(request, destinatario_id):
    destinatario = User.objects.get(id=destinatario_id)

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():            
            mensaje_enviado = Mensaje(remitente=request.user, destinatario=destinatario, contenido=form.cleaned_data['contenido'])
            mensaje_enviado.save()
            mensaje_recibido = Mensaje(remitente=request.user, destinatario=destinatario, contenido=form.cleaned_data['contenido'])
            mensaje_recibido.save()
            request.user.mensajes_enviados.add(mensaje_enviado)
            request.user.mensajes_recibidos.add(mensaje_recibido)            
            messages.success(request, '¡Mensaje enviado con éxito!')
            return redirect('mensajes')
    else:
        form = MensajeForm()
    
    return render(request, 'blog/enviar_mensaje.html', {'form': form, 'destinatario': destinatario})

@login_required
def mensajes(request):
    print(request.user)
    mensajes_enviados = Mensaje.objects.filter(remitente=request.user)
    mensajes_recibidos = request.user.mensajes_recibidos.all()
    users = User.objects.exclude(id=request.user.id)
    print(mensajes_enviados)  

    return render(request, 'blog/mensajes.html', {'mensajes_enviados': mensajes_enviados, 'mensajes_recibidos': mensajes_recibidos, 'users': users})



def crear_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            # Establecer el autor del blog como el usuario actual
            blog.autor = request.user
            blog.save()
            return redirect('listar_blogs')
    else:
        form = BlogForm()
    
    return render(request, 'blog/crear_blog.html', {'form': form})


def editar_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            if 'imagen' in request.FILES:
                blog.imagen = request.FILES['imagen']
            blog = form.save()
            return redirect('listar_blogs')
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'blog/editar_blog.html', {'form': form, 'blog': blog})


def eliminar_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    if request.method == 'POST':
        blog.delete()
        return redirect('listar_blogs')
    
    return render(request, 'blog/eliminar_blog.html', {'blog': blog})


@login_required
def editar_perfil(request):
    perfil = request.user.perfil

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'blog/editar_perfil.html', {'form': form})

@login_required
def borrar_perfil(request):
    perfil = request.user.perfil

    if request.method == 'POST':
        perfil.delete()
        return redirect('logout')

    return render(request, 'blog/borrar_perfil.html')


class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

def logout_view(request):
    logout(request)
    # Redirige a la página de inicio o a cualquier otra página deseada
    return redirect('inicio')    


def ver_mensaje(request, mensaje_id):
    mensaje = get_object_or_404(Mensaje, id=mensaje_id)
    return render(request, 'blog/detalle_mensaje.html', {'mensaje': mensaje})