from rest_framework import serializers
from django.utils import timezone
from .models import Usuario, Paciente, Administrador, ProfissionalSaude, Consulta, LogAcao


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "email", "papel"]


class PacienteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    senha = serializers.CharField(write_only=True, required=True, min_length=6)
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Paciente
        fields = [
            "id", "usuario", "email", "senha",
            "nome_completo", "cpf", "data_nascimento",
            "telefone", "endereco", "criado_em", "atualizado_em"
        ]
        read_only_fields = ["criado_em", "atualizado_em"]

    def create(self, validated_data):
        email = validated_data.pop("email")
        senha = validated_data.pop("senha")

        usuario = Usuario.objects.create_user(
            email=email,
            password=senha,
            papel=Usuario.PAPEL_PACIENTE,
        )
        paciente = Paciente.objects.create(usuario=usuario, **validated_data)
        return paciente

    def update(self, instance, validated_data):
        email = validated_data.pop("email", None)
        senha = validated_data.pop("senha", None)

        if email:
            instance.usuario.email = email
            instance.usuario.save()
        if senha:
            instance.usuario.set_password(senha)
            instance.usuario.save()

        return super().update(instance, validated_data)


class AdministradorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    senha = serializers.CharField(write_only=True, required=True, min_length=6)
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Administrador
        fields = [
            "id", "usuario", "email", "senha",
            "nome_completo", "cargo", "criado_em", "atualizado_em"
        ]
        read_only_fields = ["criado_em", "atualizado_em"]

    def create(self, validated_data):
        email = validated_data.pop("email")
        senha = validated_data.pop("senha")

        usuario = Usuario.objects.create_user(
            email=email,
            password=senha,
            papel=Usuario.PAPEL_ADMIN,
            is_staff=True,
        )
        administrador = Administrador.objects.create(usuario=usuario, **validated_data)
        return administrador

    def update(self, instance, validated_data):
        email = validated_data.pop("email", None)
        senha = validated_data.pop("senha", None)

        if email:
            instance.usuario.email = email
            instance.usuario.save()
        if senha:
            instance.usuario.set_password(senha)
            instance.usuario.save()

        return super().update(instance, validated_data)


class ProfissionalSaudeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    senha = serializers.CharField(write_only=True, required=True, min_length=6)
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = ProfissionalSaude
        fields = [
            "id", "usuario", "email", "senha",
            "nome_completo", "especialidade", "registro_profissional",
            "criado_em", "atualizado_em"
        ]
        read_only_fields = ["criado_em", "atualizado_em"]

    def create(self, validated_data):
        email = validated_data.pop("email")
        senha = validated_data.pop("senha")

        usuario = Usuario.objects.create_user(
            email=email,
            password=senha,
            papel=Usuario.PAPEL_PROFISSIONAL,
        )
        profissional = ProfissionalSaude.objects.create(usuario=usuario, **validated_data)
        return profissional

    def update(self, instance, validated_data):
        email = validated_data.pop("email", None)
        senha = validated_data.pop("senha", None)

        if email:
            instance.usuario.email = email
            instance.usuario.save()
        if senha:
            instance.usuario.set_password(senha)
            instance.usuario.save()

        return super().update(instance, validated_data)


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = [
            "id", "paciente", "profissional", "administrador_criador",
            "tipo_atendimento", "data_horario", "local",
            "link_teleconsulta", "status", "justificativa_cancelamento",
            "criado_em", "atualizado_em"
        ]
        read_only_fields = [
            "administrador_criador", "link_teleconsulta",
            "status", "justificativa_cancelamento",
            "criado_em", "atualizado_em"
        ]

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("A data/hora da consulta deve ser no futuro.")
        return value


class LogAcaoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = LogAcao
        fields = ["id", "usuario", "acao", "detalhes", "data_hora", "ip"]
