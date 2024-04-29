
from .decorators import verificar_autenticacion
from .models import Evento,Usuario

@verificar_autenticacion
def cantidad_eventos_usuario(request):
    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(codigo=usuario_id)
    
    #CONSULTA AVANZADA( CANTIDAD DE EVENTOS REALIZADOS )
    cantidad_eventos_usuario = Evento.objects.filter(encargado=usuario).count()
    #CONSULTA AVANZADA( CANTIDAD DE EVENTOS REALIZADOS )

    return {'cantidad_eventos_usuario': cantidad_eventos_usuario}