from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    
    path('',views.index,name='index'),
    
    #ACCIONES DE USUARIO
    path('iniciarsesion/',views.login,name='iniciarsesion'),
    path('registrar/',views.signup,name='registrar'),
    path('cerrarsesion/', views.cerrar_sesion, name='cerrar_sesion'),
    
    #ACCIONES DE EVENTO
    path('eventos/',views.evento,name='eventos'),
    path('miseventos/', views.mis_eventos, name='mis_eventos'),
    path('actualizarMiEvento/', views.actualizar_mi_evento, name='actualizar_mi_evento'),
    path('detalle_evento/eliminarMiEvento/<int:evento_codigo>/',views.eliminar_mi_evento,name='eliminar_mi_evento'),
     
    path('detalle_evento/<int:evento_codigo>/',views.detalle_evento,name='detalle_evento'),
    path('agregarEvento/',views.agregar_evento,name='agregar_evento'),
    path('detalle_evento/eliminarEvento/<int:evento_codigo>/',views.eliminar_evento,name='eliminar_evento'),
    path('actualizarEvento/', views.actualizar_evento, name='actualizar_evento'),

    #ACCIONES DE REGISTRO DE USUARIO EN EVENTO
    path('registrar_usuario_evento/', views.registrar_usuario_evento, name='registrar_usuario_evento'),
    path('agregar_usuario_evento/', views.agregar_usuario_evento, name='agregar_usuario_evento'),
    path('eliminar_usuario_evento/<int:evento_codigo>/<int:usuario_codigo>/', views.eliminar_usuario_evento, name='eliminar_usuario_evento'),
    
]