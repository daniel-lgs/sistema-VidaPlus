from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LoginView,
    LogoutView,
    PacienteViewSet,
    AdministradorViewSet,
    ProfissionalSaudeViewSet,
    ConsultaViewSet,
    LogAcaoViewSet,
)

router = DefaultRouter()
router.register(r"pacientes", PacienteViewSet, basename="pacientes")
router.register(r"administradores", AdministradorViewSet, basename="administradores")
router.register(r"profissionais-saude", ProfissionalSaudeViewSet, basename="profissionais-saude")
router.register(r"consultas", ConsultaViewSet, basename="consultas")
router.register(r"logs", LogAcaoViewSet, basename="logs")

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("", include(router.urls)),
]
