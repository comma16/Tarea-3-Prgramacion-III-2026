from datetime import datetime
import re


def formatear_fecha(fecha_str, formato_entrada=None, formato_salida="%Y-%m-%d"):
    """
    Convierte una fecha string a formato estándar ISO 8601.
    Detecta automáticamente el formato de entrada si no se especifica.
    """
    formatos_comunes = [
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%Y-%m-%d",
        "%d %b %Y",
        "%B %d, %Y",
    ]

    if formato_entrada:
        try:
            fecha = datetime.strptime(fecha_str.strip(), formato_entrada)
            return fecha.strftime(formato_salida)
        except ValueError:
            raise ValueError(f"La fecha '{fecha_str}' no coincide con el formato '{formato_entrada}'.")

    for fmt in formatos_comunes:
        try:
            fecha = datetime.strptime(fecha_str.strip(), fmt)
            return fecha.strftime(formato_salida)
        except ValueError:
            continue

    raise ValueError(f"No se pudo detectar el formato de la fecha: '{fecha_str}'")


def validar_fecha(fecha_str):
    patron = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(patron, fecha_str):
        return False
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def fecha_a_legible(fecha_str):
    meses = [
        "", "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    return f"{fecha.day} de {meses[fecha.month]} de {fecha.year}"
