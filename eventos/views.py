from django.shortcuts import get_object_or_404, render, redirect
from .models import Usuario,Evento,RegistroEvento
from django.contrib import messages
from .decorators import verificar_autenticacion
import calendar
from datetime import datetime
from django.db.models import Count

def index(request):
    if 'usuario_id' in request.session:
        # Si el usuario está autenticado, puedes obtener más información del usuario si es necesario
        usuario_id = request.session['usuario_id']
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            # Hacer algo con los datos del usuario si es necesario
        except Usuario.DoesNotExist:
            pass
    return render(request, 'index.html')

#ACCIONES USUARIO

def signup(request):
    nombre = request.POST.get('nombre')
    apellido = request.POST.get('apellido')
    email = request.POST.get('email')
    contraseña = request.POST.get('contraseña')
        
    if Usuario.objects.filter(email=email).exists():
        messages.error(request, 'El usuario con este correo electrónico ya existe.')
        return render(request,'register.html')
        
    Usuario.objects.create(nombre=nombre, apellido=apellido, email=email, contraseña=contraseña)
        
    return redirect('/eventos/iniciarsesion')

def login(request):
    
    email = request.POST.get('email')
    contraseña = request.POST.get('contraseña')
        
    if Usuario.objects.filter(email=email).exists():
        usuario = Usuario.objects.get(email=email)
        if usuario.contraseña == contraseña:
            request.session['usuario_id'] = usuario.codigo  
            return redirect('/eventos/eventos')
        else:
            messages.error(request, 'Contraseña incorrecta.')
            return render(request, 'login.html')
            
    else:
        if Usuario.DoesNotExist:
            messages.error(request, 'La cuenta no existe.')
            return render(request, 'login.html')

    return render(request, 'login.html')

def cerrar_sesion(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    return redirect('/eventos/iniciarsesion/')


#ACCIONES EVENTO

@verificar_autenticacion
def evento(request):
    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(codigo=usuario_id)
    evento_lista = Evento.objects.all()
    
    #CONSULTA AVANZADA (CANTIDAD DE EVENTOS EN EL MES)
    actual = datetime.now()
    primer_dia_mes_actual = datetime(actual.year, actual.month, 1)
    ultimo_dia_mes_actual = datetime(actual.year, actual.month, calendar.monthrange(actual.year, actual.month)[1])

    eventos_mes_actual = Evento.objects.filter(fecha_evento__gte=primer_dia_mes_actual, fecha_evento__lte=ultimo_dia_mes_actual)
    cantidad_eventos_mes_actual = eventos_mes_actual.count()
    #CONSULTA AVANZADA (CANTIDAD DE EVENTOS EN EL MES)
    
    #CONSULTA AVANZADA (USUARIOS CON MAYOR PARTICIPACION)
    usuarios_mas_registrados = Usuario.objects.annotate(num_registros=Count('registroevento')).order_by('-num_registros')
    #CONSULTA AVANZADA (USUARIO CON MAYOR PARTICIPACION)
    
    for evento in evento_lista:
        if usuario == evento.encargado:
            evento.es_encargado = True
        else:
            evento.es_encargado = False

    context = {
        'evento_lista': evento_lista,
        'usuario': usuario,
        'cantidad_eventos_mes_actual': cantidad_eventos_mes_actual,
        'usuarios_mas_registrados': usuarios_mas_registrados,
    }
    return render(request, 'eventos.html', context)

@verificar_autenticacion
def agregar_evento(request):
    titulo = request.POST['titulo']
    encargado_id = request.POST['encargado']  
    encargado = Usuario.objects.get(codigo=encargado_id)  
    imagen = request.FILES['imagen']
    fecha_evento = request.POST['fecha_evento']
    hora_evento = request.POST['hora_evento']
    descripcion = request.POST['descripcion']
    
    Evento.objects.create(titulo=titulo, encargado=encargado, imagen=imagen, fecha_evento=fecha_evento, hora_evento=hora_evento, descripcion=descripcion)
        
    return redirect('/eventos/eventos')

@verificar_autenticacion
def detalle_evento(request, evento_codigo):
    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(codigo=usuario_id)
    evento = get_object_or_404(Evento, codigo=evento_codigo)
    usuario_lista = Usuario.objects.all()
    
    registros_evento = RegistroEvento.objects.filter(evento=evento)
    
    usuarios_registrados = [registro.usuario for registro in registros_evento]
    
    #CONSULTA AVANZADA (CANTIDAD DE USUARIOS REGISTRADOS EN EL EVENTO)
    cantidad_usuarios_registrados = len(usuarios_registrados)
    #CONSULTA AVANZADA (CANTIDAD DE USUARIOS REGISTRADOS EN EL EVENTO)
    
    if usuario == evento.encargado:
        es_encargado = True
    else:
        es_encargado = False

    context = {
        'evento': evento,
        'es_encargado': es_encargado,
        'usuario': usuario,
        'usuario_lista':usuario_lista,
        'usuarios_registrados': usuarios_registrados,
        'cantidad_usuarios_registrados': cantidad_usuarios_registrados,
    }
    
    return render(request, 'detalleEvento.html', context)

@verificar_autenticacion
def actualizar_evento(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        titulo = request.POST['titulo']
        encargado_id = request.POST['encargado']
        encargado = Usuario.objects.get(codigo=encargado_id)

        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
        else:
            evento = Evento.objects.get(codigo=codigo)
            imagen = evento.imagen  

        fecha_evento = request.POST['fecha_evento']
        hora_evento = request.POST['hora_evento']
        descripcion = request.POST['descripcion']

        evento = Evento.objects.get(codigo=codigo)

        evento.titulo = titulo
        evento.encargado = encargado
        evento.imagen = imagen
        evento.fecha_evento = fecha_evento
        evento.hora_evento = hora_evento
        evento.descripcion = descripcion

        evento.save()

        return redirect('/eventos/detalle_evento/{}/'.format(codigo))
    else:
        return redirect('/eventos/detalle_evento/{}/'.format(codigo))

@verificar_autenticacion 
def eliminar_evento(request, evento_codigo):
    evento = Evento.objects.get(codigo=evento_codigo)
    evento.delete()
    
    return redirect('/eventos/eventos')

@verificar_autenticacion
def mis_eventos(request):
    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(codigo=usuario_id)

    eventos_usuario = Evento.objects.filter(encargado=usuario)

    #CONSULTA AVANZADA (CANTIDAD DE EVENTOS ORGANIZADOS)
    cantidad_eventos_usuario = eventos_usuario.count()
    #CONSULTA AVANZADA (CANTIDAD DE EVENTOS ORGANIZADOS)
    
    context = {
        'eventos_usuario': eventos_usuario,
        'usuario': usuario,
        'cantidad_eventos_usuario': cantidad_eventos_usuario,
    }
    return render(request, 'misEventos.html', context)

@verificar_autenticacion
def actualizar_mi_evento(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        titulo = request.POST['titulo']
        encargado_id = request.POST['encargado']
        encargado = Usuario.objects.get(codigo=encargado_id)

        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
        else:
            evento = Evento.objects.get(codigo=codigo)
            imagen = evento.imagen  

        fecha_evento = request.POST['fecha_evento']
        hora_evento = request.POST['hora_evento']
        descripcion = request.POST['descripcion']

        evento = Evento.objects.get(codigo=codigo)

        evento.titulo = titulo
        evento.encargado = encargado
        evento.imagen = imagen
        evento.fecha_evento = fecha_evento
        evento.hora_evento = hora_evento
        evento.descripcion = descripcion

        evento.save()

        return redirect('/eventos/miseventos/')
    else:
        return redirect('/eventos/miseventos')

@verificar_autenticacion 
def eliminar_mi_evento(request, evento_codigo):
    evento = Evento.objects.get(codigo=evento_codigo)
    evento.delete()
    
    return redirect('/eventos/miseventos/')

#REGISTRAR USUARIOS EN EVENTOS 

@verificar_autenticacion
def registrar_usuario_evento(request):
    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(codigo=usuario_id)
    evento_id = request.POST['evento_id']
    evento = get_object_or_404(Evento, codigo=evento_id)
        
    if RegistroEvento.objects.filter(evento=evento, usuario=usuario).exists():
        messages.error(request, 'Ya estás registrado para este evento.')
    else:
        RegistroEvento.objects.create(evento=evento, usuario=usuario)
        messages.success(request, 'Te has registrado exitosamente para el evento.')
        
    return redirect('/eventos/eventos')

@verificar_autenticacion
def agregar_usuario_evento(request):
    evento_codigo = request.POST.get('codigo')
    usuario_codigo = request.POST.get('usuario_codigo')  
        
    evento = Evento.objects.get(codigo=evento_codigo)
    usuario = Usuario.objects.get(codigo=usuario_codigo)
        
    RegistroEvento.objects.create(evento=evento, usuario=usuario)
        
    return redirect('/eventos/detalle_evento/{}/'.format(evento_codigo)) 

@verificar_autenticacion
def eliminar_usuario_evento(request,usuario_codigo,evento_codigo):
    
    registro_evento = RegistroEvento.objects.get(evento=evento_codigo, usuario=usuario_codigo)
    
    registro_evento.delete()
        
    return redirect('/eventos/detalle_evento/{}'.format(evento_codigo))  
