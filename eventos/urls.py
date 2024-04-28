from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    path('',views.index,name='index'),
    
    #ACCIONES DE USUARIO
    path('iniciarsesion/',views.login,name='iniciarsesion'),
    path('registrar/',views.signup,name='registrar'),
    
    #ACCIONES DE EVENTO
    path('eventos/',views.evento,name='eventos'),
    path('detalle_evento/<int:evento_id>/',views.detalle_evento,name='detalle_evento'),
    path('agregarEvento/',views.agregar_evento,name='agregar_evento'),
    path('detalle_evento/eliminarEvento/<int:evento_id>/',views.eliminar_evento,name='eliminar_evento'),
    path('actualizarEvento/', views.actualizar_evento, name='actualizar_evento'),

    
    
]