from django.core.management.base import BaseCommand
from core.models import Usuario, Administrador


class Command(BaseCommand):
    help = "Cria o usuário administrador inicial do sistema SGHSS."

    def handle(self, *args, **options):
        email = "sistema.sghss@gmail.com"
        senha = "dSf@#4340fdk"

        if Usuario.objects.filter(email=email).exists():
            usuario = Usuario.objects.get(email=email)
            self.stdout.write(
                self.style.WARNING(
                    f"Usuário admin com e-mail {email} já existe (id={usuario.id})."
                )
            )
            return

        usuario = Usuario.objects.create_superuser(
            email=email,
            password=senha,
            papel=Usuario.PAPEL_ADMIN,
        )

        Administrador.objects.create(
            usuario=usuario,
            nome_completo="Administrador Principal",
            cargo="Administrador do Sistema",
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Administrador inicial criado com sucesso!\n"
                f"E-mail: {email}\nSenha: {senha}"
            )
        )
