from django.contrib import admin
from .models import Usuario, Evento, RegistroEvento

admin.site.register(Usuario)
admin.site.register(Evento)
admin.site.register(RegistroEvento)

