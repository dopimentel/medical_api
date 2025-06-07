from django.db import models
from django.core.exceptions import ValidationError
from professionals.models import Professional


class Appointment(models.Model):
    """
    Model representing medical appointments.
    """

    date = models.DateTimeField("Data da Consulta")
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Profissional",
    )
    notes = models.TextField("Observações", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        ordering = ["-date"]

    def __str__(self):
        return f"Consulta com {self.professional.name} em {self.date.strftime('%d/%m/%Y %H:%M')}"

    def clean(self):
        """Valida se já existe consulta para este profissional neste horário"""
        if self.date and self.professional:
            # Verificar se já existe uma consulta para este profissional neste horário
            overlapping_appointments = Appointment.objects.filter(
                professional=self.professional, date=self.date
            ).exclude(id=self.id)

            if overlapping_appointments.exists():
                raise ValidationError(
                    {
                        "date": "Já existe uma consulta marcada para este profissional neste horário."
                    }
                )
