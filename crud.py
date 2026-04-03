from django.db import models
from django.contrib.auth.hashers import make_password


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "usuarios"
        ordering = ["-fecha_creacion"]
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.username})"

    def save(self, *args, **kwargs):
        if not self.pk and self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


def crear_usuario(nombre, apellido, email, username, password):
    usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        email=email,
        username=username,
        password=password,
    )
    usuario.save()
    return usuario


def obtener_usuario(usuario_id):
    try:
        return Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        return None


def listar_usuarios():
    return Usuario.objects.filter(activo=True)


def actualizar_usuario(usuario_id, **kwargs):
    Usuario.objects.filter(pk=usuario_id).update(**kwargs)
    return obtener_usuario(usuario_id)


def eliminar_usuario(usuario_id):
    Usuario.objects.filter(pk=usuario_id).update(activo=False)
