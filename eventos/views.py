from django.shortcuts import get_object_or_404, render, redirect
from .models import Usuario,Evento,RegistroEvento
from django.contrib import messages
from .decorators import verificar_autenticacion

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        contraseña = request.POST.get('contraseña')
        
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El usuario con este correo electrónico ya existe.')
            return render(request,'register.html')
        
        usuario = Usuario.objects.create(nombre=nombre, apellido=apellido, email=email, contraseña=contraseña)
        
        return redirect('/eventos/iniciarsesion')
    else:
        
        return render(request,'register.html')

def login(request):
    
    if request.method == 'POST':
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

@verificar_autenticacion
def evento(request):
    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(pk=usuario_id)
    evento_lista = Evento.objects.all()
    registro_usuario_evento = RegistroEvento.objects.all()

    for evento in evento_lista:
        if usuario == evento.encargado:
            evento.es_encargado = True
        else:
            evento.es_encargado = False

    context = {
        'evento_lista': evento_lista,
        'usuario': usuario,
    }
    return render(request, 'eventos.html', context)

def agregar_evento(request):
    titulo = request.POST['titulo']
    encargado_id = request.POST['encargado']  
    encargado = Usuario.objects.get(codigo=encargado_id)  
    imagen = request.FILES['imagen']
    fecha_evento = request.POST['fecha_evento']
    hora_evento = request.POST['hora_evento']
    descripcion = request.POST['descripcion']
    
    evento = Evento.objects.create(titulo=titulo, encargado=encargado, imagen=imagen, fecha_evento=fecha_evento, hora_evento=hora_evento, descripcion=descripcion)
        
    return redirect('/eventos/eventos')

@verificar_autenticacion
def detalle_evento(request, evento_id):
    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(codigo=usuario_id)
    evento = get_object_or_404(Evento, codigo=evento_id)

    if usuario == evento.encargado:
        es_encargado = True
    else:
        es_encargado = False

    context = {
        'evento': evento,
        'es_encargado': es_encargado,
        'usuario': usuario,
    }
    
    return render(request, 'detalleEvento.html', context)

def actualizar_evento(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        titulo = request.POST['titulo']
        encargado_id = request.POST['encargado']
        encargado = Usuario.objects.get(codigo=encargado_id)

        # Verifica si se proporciona una nueva imagen
        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
        else:
            evento = Evento.objects.get(codigo=codigo)
            imagen = evento.imagen  # Mantén la imagen existente

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
    
def eliminar_evento(request, evento_id):
    evento = Evento.objects.get(codigo=evento_id)
    evento.delete()
    
    return redirect('/eventos/eventos')

@verificar_autenticacion
def registrar_usuario_evento(request):
    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(pk=usuario_id)
    evento_id = request.POST['evento_id']
    evento = get_object_or_404(Evento, codigo=evento_id)
        
    # Verificar si el usuario ya está registrado para este evento
    if RegistroEvento.objects.filter(evento=evento, usuario=usuario).exists():
        messages.error(request, 'Ya estás registrado para este evento.')
    else:
    # Si el usuario no está registrado, crear una instancia de RegistroEvento
        registro = RegistroEvento.objects.create(evento=evento, usuario=usuario)
        messages.success(request, 'Te has registrado exitosamente para el evento.')
        
    return redirect('/eventos/eventos')