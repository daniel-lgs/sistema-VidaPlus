from django.contrib import admin
from .models import Usuario, Paciente, Administrador, ProfissionalSaude, Consulta, LogAcao


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "papel", "is_staff", "is_active")
    search_fields = ("email",)
    list_filter = ("papel", "is_staff", "is_active")


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nome_completo", "cpf", "usuario")
    search_fields = ("nome_completo", "cpf", "usuario__email")


@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ("id", "nome_completo", "cargo", "usuario")
    search_fields = ("nome_completo", "usuario__email")


@admin.register(ProfissionalSaude)
class ProfissionalSaudeAdmin(admin.ModelAdmin):
    list_display = ("id", "nome_completo", "especialidade", "registro_profissional", "usuario")
    search_fields = ("nome_completo", "especialidade", "registro_profissional", "usuario__email")


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ("id", "paciente", "profissional", "tipo_atendimento", "data_horario", "status")
    list_filter = ("tipo_atendimento", "status")
    search_fields = ("paciente__nome_completo", "profissional__nome_completo")


@admin.register(LogAcao)
class LogAcaoAdmin(admin.ModelAdmin):
    list_display = ("id", "data_hora", "usuario", "acao", "ip")
    list_filter = ("acao",)
    search_fields = ("acao", "usuario__email", "detalhes")
