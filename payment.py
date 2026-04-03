import uuid
from django.db import models
from django.utils import timezone


class Pago(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("completado", "Completado"),
        ("fallido", "Fallido"),
        ("reembolsado", "Reembolsado"),
    ]

    referencia = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    usuario = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="pagos"
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3, default="USD")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="pendiente")
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pagos"
        ordering = ["-fecha_creacion"]
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"Pago {self.referencia} - {self.estado}"


def procesar_pago(usuario_id, monto, descripcion=""):
    pago = Pago.objects.create(
        usuario_id=usuario_id,
        monto=monto,
        descripcion=descripcion,
        estado="pendiente",
    )
    # Simulación de procesamiento
    if monto > 0:
        pago.estado = "completado"
    else:
        pago.estado = "fallido"
    pago.save()
    return pago


def obtener_pagos_usuario(usuario_id):
    return Pago.objects.filter(usuario_id=usuario_id).order_by("-fecha_creacion")


def reembolsar_pago(pago_id):
    try:
        pago = Pago.objects.get(pk=pago_id, estado="completado")
        pago.estado = "reembolsado"
        pago.save()
        return pago
    except Pago.DoesNotExist:
        return None

