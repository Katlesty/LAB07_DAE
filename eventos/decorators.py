from django.shortcuts import redirect
from functools import wraps
from .models import Usuario

def verificar_autenticacion(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' in request.session:
            usuario_id = request.session['usuario_id']
            try:
                usuario = Usuario.objects.get(pk=usuario_id)
                return view_func(request, *args, **kwargs)
            except Usuario.DoesNotExist:
                pass
        return redirect('/iniciarsesion/')
    return wrapper