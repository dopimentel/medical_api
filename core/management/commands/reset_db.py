"""
Command for resetting the database and loading initial data.
"""

import logging
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.core.management import call_command
from professionals.models import Professional
from appointments.models import Appointment
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Reset database, run migrations and populate with initial data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-input",
            action="store_true",
            help="Do not prompt user for input",
        )
        parser.add_argument(
            "--no-seed",
            action="store_true",
            help="Do not seed initial data",
        )

    def handle(self, *args, **options):
        no_input = options["no_input"]
        no_seed = options["no_seed"]

        if not no_input:
            self.stdout.write(
                self.style.WARNING(
                    "Você está prestes a APAGAR e recriar o banco de dados!"
                )
            )
            answer = input("Você tem certeza que deseja continuar? (y/n): ")
            if answer.lower() != "y":
                self.stdout.write(
                    self.style.SUCCESS("Operação cancelada pelo usuário.")
                )
                return

        try:
            self.reset_database()
            self.stdout.write(
                self.style.SUCCESS("Banco de dados resetado com sucesso!")
            )

            if not no_seed:
                self.seed_data()
                self.stdout.write(
                    self.style.SUCCESS("Dados iniciais carregados com sucesso!")
                )
        except Exception as e:
            raise CommandError(f"Erro ao resetar o banco de dados: {e}")

    def reset_database(self):
        """
        Reset the database by reversing all migrations and then reapplying them.
        """
        # Terminar todas as conexões ao banco de dados para evitar bloqueios
        self.stdout.write(self.style.NOTICE("Terminando conexões abertas..."))
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT pg_terminate_backend(pid) 
                    FROM pg_stat_activity 
                    WHERE datname = current_database() AND pid <> pg_backend_pid()
                    """
                )
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Erro ao terminar conexões: {e}"))

        # Reverter todas as migrações
        self.stdout.write(self.style.NOTICE("Revertendo migrações..."))

        # Reverter migrações por app
        apps = [
            "appointments",
            "professionals",
            "sessions",
            "admin",
            "auth",
            "contenttypes",
        ]

        for app in apps:
            try:
                self.stdout.write(f"Revertendo migrações para {app}...")
                call_command("migrate", app, "zero", "--no-input")
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Erro ao reverter {app}: {e}"))

        # Aplicar todas as migrações novamente
        self.stdout.write(self.style.NOTICE("Aplicando migrações..."))
        call_command("migrate", "--no-input")

    def seed_data(self):
        """Seed the database with initial data."""
        # self.stdout.write(self.style.NOTICE("Criando superusuário..."))
        # call_command(
        #     "createsuperuser",
        #     "--username=admin",
        #     "--email=admin@example.com",
        #     "--no-input",
        # )

        self.stdout.write(self.style.NOTICE("Criando profissionais..."))
        self.create_professionals()

        self.stdout.write(self.style.NOTICE("Criando consultas..."))
        self.create_appointments()

    def create_professionals(self):
        """Create initial professionals."""
        professionals_data = [
            {
                "preferred_name": "Dra. Ana Silva",
                "profession": "Cardiologista",
                "address": "Av. Paulista, 1000, São Paulo - SP",
                "contact": "11999991111",
            },
            {
                "preferred_name": "Dr. Carlos Oliveira",
                "profession": "Dermatologista",
                "address": "Rua Augusta, 500, São Paulo - SP",
                "contact": "11999992222",
            },
            {
                "preferred_name": "Dra. Mariana Souza",
                "profession": "Neurologista",
                "address": "Av. Brasil, 300, Rio de Janeiro - RJ",
                "contact": "21999993333",
            },
            {
                "preferred_name": "Dr. João Castro",
                "profession": "Oftalmologista",
                "address": "Rua das Flores, 200, Belo Horizonte - MG",
                "contact": "31999994444",
            },
            {
                "preferred_name": "Dra. Fernanda Lima",
                "profession": "Psiquiatra",
                "address": "Av. Atlântica, 800, Rio de Janeiro - RJ",
                "contact": "21999995555",
            },
        ]

        for data in professionals_data:
            Professional.objects.create(**data)
            self.stdout.write(
                self.style.SUCCESS(f"Profissional {data['preferred_name']} criado!")
            )

    def create_appointments(self):
        """Create initial appointments."""
        professionals = Professional.objects.all()

        if not professionals.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Nenhum profissional encontrado para criar consultas."
                )
            )
            return

        # Data base (hoje) para criar consultas
        base_date = datetime.now()

        # Para cada profissional, criar 3 consultas
        for professional in professionals:
            # Criar consulta para hoje
            Appointment.objects.create(
                professional=professional,
                date=base_date.replace(hour=10, minute=0, second=0, microsecond=0),
            )

            # Criar consulta para amanhã
            tomorrow = base_date + timedelta(days=1)
            Appointment.objects.create(
                professional=professional,
                date=tomorrow.replace(hour=14, minute=30, second=0, microsecond=0),
            )

            # Criar consulta para próxima semana
            next_week = base_date + timedelta(days=7)
            Appointment.objects.create(
                professional=professional,
                date=next_week.replace(hour=16, minute=0, second=0, microsecond=0),
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Consultas criadas para {professional.preferred_name}!"
                )
            )
