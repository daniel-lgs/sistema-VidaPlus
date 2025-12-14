from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    """
    Gerenciador customizado para o modelo de usuário baseado em e-mail.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O campo e-mail é obrigatório.")
        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("papel", Usuario.PAPEL_ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuário deve ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuário deve ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    """
    Modelo de usuário customizado usando e-mail como identificador principal
    e com um campo 'papel' para diferenciar Administrador, Paciente e Profissional de Saúde.
    """

    username = None
    email = models.EmailField("e-mail", unique=True)

    PAPEL_ADMIN = "ADMIN"
    PAPEL_PACIENTE = "PACIENTE"
    PAPEL_PROFISSIONAL = "PROF"

    PAPEL_CHOICES = [
        (PAPEL_ADMIN, "Administrador"),
        (PAPEL_PACIENTE, "Paciente"),
        (PAPEL_PROFISSIONAL, "Profissional de Saúde"),
    ]

    papel = models.CharField("papel", max_length=20, choices=PAPEL_CHOICES)

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.get_papel_display()})"


class Paciente(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil_paciente",
    )
    nome_completo = models.CharField("Nome completo", max_length=255)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    data_nascimento = models.DateField("Data de nascimento")
    telefone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    endereco = models.CharField("Endereço", max_length=255, blank=True, null=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return f"{self.nome_completo} - {self.cpf}"


class Administrador(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil_administrador",
    )
    nome_completo = models.CharField("Nome completo", max_length=255)
    cargo = models.CharField("Cargo", max_length=100, default="Administrador")
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return f"{self.nome_completo} ({self.cargo})"


class ProfissionalSaude(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil_profissional",
    )
    nome_completo = models.CharField("Nome completo", max_length=255)
    especialidade = models.CharField("Especialidade", max_length=100)
    registro_profissional = models.CharField(
        "Registro profissional (CRM/COREN/Outro)", max_length=50
    )
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return f"{self.nome_completo} - {self.especialidade}"


class Consulta(models.Model):
    TIPO_PRESENCIAL = "PRESENCIAL"
    TIPO_ONLINE = "ONLINE"

    TIPO_CHOICES = [
        (TIPO_PRESENCIAL, "Presencial"),
        (TIPO_ONLINE, "Online"),
    ]

    STATUS_AGENDADA = "AGENDADA"
    STATUS_CANCELADA_PACIENTE = "CANCELADA_PACIENTE"
    STATUS_CANCELADA_PROFISSIONAL = "CANCELADA_PROFISSIONAL"
    STATUS_CANCELADA_ADMIN = "CANCELADA_ADMIN"
    STATUS_REALIZADA = "REALIZADA"

    STATUS_CHOICES = [
        (STATUS_AGENDADA, "Agendada"),
        (STATUS_CANCELADA_PACIENTE, "Cancelada pelo paciente"),
        (STATUS_CANCELADA_PROFISSIONAL, "Cancelada pelo profissional"),
        (STATUS_CANCELADA_ADMIN, "Cancelada pelo administrador"),
        (STATUS_REALIZADA, "Realizada"),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="consultas")
    profissional = models.ForeignKey(ProfissionalSaude, on_delete=models.CASCADE, related_name="consultas")
    administrador_criador = models.ForeignKey(
        Administrador,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="consultas_criadas",
    )

    tipo_atendimento = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_PRESENCIAL)
    data_horario = models.DateTimeField("Data e horário da consulta")
    local = models.CharField("Local", max_length=255, blank=True, null=True)

    link_teleconsulta = models.URLField("Link da teleconsulta", blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_AGENDADA)
    justificativa_cancelamento = models.TextField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consulta {self.id} - {self.paciente} com {self.profissional} em {self.data_horario}"


class LogAcao(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs",
    )
    acao = models.CharField(max_length=255)
    detalhes = models.TextField(blank=True, null=True)
    data_hora = models.DateTimeField(default=timezone.now)
    ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"[{self.data_hora}] {self.usuario} - {self.acao}"
