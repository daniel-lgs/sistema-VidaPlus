import random
import string

from django.db import transaction
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Usuario, Paciente, Administrador, ProfissionalSaude, Consulta, LogAcao
from .permissions import EhAdministrador
from .serializers import (
    UsuarioSerializer, PacienteSerializer, AdministradorSerializer,
    ProfissionalSaudeSerializer, ConsultaSerializer, LogAcaoSerializer
)


def gerar_nome_sala_aleatorio():
    letras = string.ascii_lowercase
    grupos = []
    for _ in range(3):
        grupos.append("".join(random.choice(letras) for _ in range(3)))
    return "-".join(grupos)


def registrar_log(usuario, acao, detalhes="", ip=None):
    LogAcao.objects.create(
        usuario=usuario if usuario and getattr(usuario, "is_authenticated", False) else None,
        acao=acao,
        detalhes=detalhes,
        data_hora=timezone.now(),
        ip=ip,
    )


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        senha = request.data.get("senha")

        if not email or not senha:
            return Response({"detalhe": "Informe e-mail e senha."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({"detalhe": "Credenciais inválidas."}, status=status.HTTP_400_BAD_REQUEST)

        if not usuario.check_password(senha):
            return Response({"detalhe": "Credenciais inválidas."}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=usuario)

        registrar_log(usuario, "LOGIN", "Usuário realizou login no sistema.", request.META.get("REMOTE_ADDR"))

        return Response({"token": token.key, "usuario": UsuarioSerializer(usuario).data})


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        registrar_log(request.user, "LOGOUT", "Usuário realizou logout do sistema.", request.META.get("REMOTE_ADDR"))
        return Response({"detalhe": "Logout realizado com sucesso."})


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.select_related("usuario").all()
    serializer_class = PacienteSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        usuario = self.request.user
        if not usuario.is_authenticated:
            return Paciente.objects.none()

        if usuario.papel == Usuario.PAPEL_ADMIN:
            return self.queryset
        if usuario.papel == Usuario.PAPEL_PACIENTE:
            return self.queryset.filter(usuario=usuario)

        return Paciente.objects.none()

    def perform_create(self, serializer):
        paciente = serializer.save()
        registrar_log(
            self.request.user if self.request.user.is_authenticated else None,
            "CRIAR_PACIENTE",
            f"Paciente {paciente.id} criado. Usuário: {paciente.usuario.email}",
            self.request.META.get("REMOTE_ADDR"),
        )

    def perform_update(self, serializer):
        paciente = serializer.save()
        registrar_log(self.request.user, "ATUALIZAR_PACIENTE", f"Paciente {paciente.id} atualizado.", self.request.META.get("REMOTE_ADDR"))

    def destroy(self, request, *args, **kwargs):
        paciente = self.get_object()
        usuario = request.user

        if usuario.papel == Usuario.PAPEL_ADMIN or paciente.usuario == usuario:
            pid = paciente.id
            response = super().destroy(request, *args, **kwargs)
            registrar_log(usuario, "EXCLUIR_PACIENTE", f"Paciente {pid} excluído.", request.META.get("REMOTE_ADDR"))
            return response

        return Response({"detalhe": "Você não tem permissão para excluir este paciente."}, status=status.HTTP_403_FORBIDDEN)


class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.select_related("usuario").all()
    serializer_class = AdministradorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, EhAdministrador]

    def perform_create(self, serializer):
        admin = serializer.save()
        registrar_log(self.request.user, "CRIAR_ADMIN", f"Administrador {admin.id} criado.", self.request.META.get("REMOTE_ADDR"))

    def perform_update(self, serializer):
        admin = serializer.save()
        registrar_log(self.request.user, "ATUALIZAR_ADMIN", f"Administrador {admin.id} atualizado.", self.request.META.get("REMOTE_ADDR"))

    def perform_destroy(self, instance):
        aid = instance.id
        instance.delete()
        registrar_log(self.request.user, "EXCLUIR_ADMIN", f"Administrador {aid} excluído.", self.request.META.get("REMOTE_ADDR"))


class ProfissionalSaudeViewSet(viewsets.ModelViewSet):
    queryset = ProfissionalSaude.objects.select_related("usuario").all()
    serializer_class = ProfissionalSaudeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, EhAdministrador]

    def perform_create(self, serializer):
        prof = serializer.save()
        registrar_log(self.request.user, "CRIAR_PROFISSIONAL", f"Profissional {prof.id} criado.", self.request.META.get("REMOTE_ADDR"))

    def perform_update(self, serializer):
        prof = serializer.save()
        registrar_log(self.request.user, "ATUALIZAR_PROFISSIONAL", f"Profissional {prof.id} atualizado.", self.request.META.get("REMOTE_ADDR"))

    def perform_destroy(self, instance):
        pid = instance.id
        instance.delete()
        registrar_log(self.request.user, "EXCLUIR_PROFISSIONAL", f"Profissional {pid} excluído.", self.request.META.get("REMOTE_ADDR"))


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.select_related("paciente", "profissional", "administrador_criador").all()
    serializer_class = ConsultaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user

        if usuario.papel == Usuario.PAPEL_ADMIN:
            return self.queryset
        if usuario.papel == Usuario.PAPEL_PACIENTE:
            return self.queryset.filter(paciente__usuario=usuario)
        if usuario.papel == Usuario.PAPEL_PROFISSIONAL:
            return self.queryset.filter(profissional__usuario=usuario)

        return Consulta.objects.none()

    @transaction.atomic
    def perform_create(self, serializer):
        usuario = self.request.user

        if usuario.papel == Usuario.PAPEL_PACIENTE:
            paciente = usuario.perfil_paciente
            consulta = serializer.save(paciente=paciente, administrador_criador=None)

        elif usuario.papel == Usuario.PAPEL_ADMIN:
            administrador = usuario.perfil_administrador
            consulta = serializer.save(administrador_criador=administrador)

        else:
            raise ValueError("Apenas pacientes e administradores podem criar consultas.")

        if consulta.tipo_atendimento == Consulta.TIPO_ONLINE and not consulta.link_teleconsulta:
            consulta.link_teleconsulta = f"https://meet.jit.si/{gerar_nome_sala_aleatorio()}"
            consulta.save()

        registrar_log(usuario, "CRIAR_CONSULTA", f"Consulta {consulta.id} criada.", self.request.META.get("REMOTE_ADDR"))

    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        consulta = self.get_object()
        usuario = request.user
        justificativa = request.data.get("justificativa")

        if usuario.papel == Usuario.PAPEL_PACIENTE:
            if consulta.paciente.usuario != usuario:
                return Response({"detalhe": "Você não pode cancelar consultas de outro paciente."}, status=status.HTTP_403_FORBIDDEN)
            consulta.status = Consulta.STATUS_CANCELADA_PACIENTE
            consulta.justificativa_cancelamento = justificativa or "Cancelado pelo paciente."

        elif usuario.papel == Usuario.PAPEL_PROFISSIONAL:
            if consulta.profissional.usuario != usuario:
                return Response({"detalhe": "Você não pode cancelar consultas de outros profissionais."}, status=status.HTTP_403_FORBIDDEN)
            if not justificativa:
                return Response({"detalhe": "Justificativa é obrigatória para cancelamento."}, status=status.HTTP_400_BAD_REQUEST)
            consulta.status = Consulta.STATUS_CANCELADA_PROFISSIONAL
            consulta.justificativa_cancelamento = justificativa

        elif usuario.papel == Usuario.PAPEL_ADMIN:
            consulta.status = Consulta.STATUS_CANCELADA_ADMIN
            consulta.justificativa_cancelamento = justificativa or "Cancelado pelo administrador."

        else:
            return Response({"detalhe": "Você não tem permissão para cancelar consultas."}, status=status.HTTP_403_FORBIDDEN)

        consulta.save()

        registrar_log(usuario, "CANCELAR_CONSULTA", f"Consulta {consulta.id} cancelada. Status: {consulta.status}", request.META.get("REMOTE_ADDR"))

        return Response(ConsultaSerializer(consulta).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detalhe": "Use o endpoint /consultas/{id}/cancelar/ para cancelar uma consulta."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class LogAcaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogAcao.objects.select_related("usuario").order_by("-data_hora")
    serializer_class = LogAcaoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, EhAdministrador]
