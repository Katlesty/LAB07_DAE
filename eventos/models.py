from django.db import models

class Usuario(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    contraseña = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre + " " + self.apellido

class Evento(models.Model):
    codigo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    encargado = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="eventos")
    fecha_evento = models.DateField('Fecha de evento')
    hora_evento = models.TimeField('Hora de evento') 
    descripcion = models.TextField()
    
    def __str__(self):
        return self.titulo
    
class RegistroEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField('Fecha de registro', auto_now_add=True)

    def __str__(self):
        return self.usuario + " registrado en  " + self.evento
