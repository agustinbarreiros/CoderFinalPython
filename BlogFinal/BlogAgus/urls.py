from django.contrib import admin
from django.urls import path
from blog import views
from blog.views import CustomLoginView, logout_view
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('acercaDe/', views.acerca_de, name='acerca_de'),
    path('pages/', views.listar_blogs, name='listar_blogs'),
    path('pages/<int:page_id>/', views.detalle_pagina, name='detalle_pagina'),
    path('inicio/', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('perfil', views.perfil, name='perfil'),
    path('enviar_mensaje/<int:destinatario_id>/', views.enviar_mensaje, name='enviar_mensaje'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('mensajes/', views.mensajes, name='mensajes'),
    path('crear_blog/', views.crear_blog, name='crear_blog'),
    path('editar_blog/<int:blog_id>/', views.editar_blog, name='editar_blog'),
    path('eliminar_blog/<int:blog_id>/', views.eliminar_blog, name='eliminar_blog'),
    path('accounts/profile/editar/', views.editar_perfil, name='editar_perfil'),
    path('accounts/profile/borrar/', views.borrar_perfil, name='borrar_perfil'),
    path('logout/', logout_view, name='logout'),
    path('mensaje/<int:mensaje_id>/', views.ver_mensaje, name='ver_mensaje')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
