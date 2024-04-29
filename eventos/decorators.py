
from functools import wraps
from .models import Usuario


def verificar_autenticacion(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('usuario_id'):
            usuario_id = request.session['usuario_id']
            try:
                usuario = Usuario.objects.get(codigo=usuario_id)
                return view_func(request, *args, **kwargs)
            except Usuario.DoesNotExist:
                pass
        return view_func(request, *args, **kwargs)
    return wrapper