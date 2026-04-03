from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone


@login_required
def dashboard_view(request):
    total_usuarios = User.objects.filter(is_active=True).count()
    nuevos_hoy = User.objects.filter(
        date_joined__date=timezone.now().date()
    ).count()
    admins = User.objects.filter(is_staff=True).count()
    ultimos_usuarios = User.objects.order_by("-date_joined")[:5]

    context = {
        "total_usuarios": total_usuarios,
        "nuevos_hoy": nuevos_hoy,
        "admins": admins,
        "ultimos_usuarios": ultimos_usuarios,
        "fecha_actual": timezone.now(),
    }
    return render(request, "dashboard.html", context)


@login_required
def perfil_view(request):
    usuario = request.user
    context = {
        "usuario": usuario,
        "fecha_union": usuario.date_joined,
        "ultimo_login": usuario.last_login,
    }
    return render(request, "perfil.html", context)
