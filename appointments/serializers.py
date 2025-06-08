from rest_framework import serializers
from .models import Appointment
from professionals.serializers import ProfessionalSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Appointment model.
    """
    professional_data = ProfessionalSerializer(source="professional", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "date",
            "professional",
            "professional_data",
        ]

    def validate(self, attrs):
        """
        Valida se já existe consulta para este profissional neste horário
        """
        date = attrs.get("date")
        professional = attrs.get("professional")
        instance = self.instance

        if date and professional:
            # Verificar se já existe consulta neste horário para este profissional
            overlapping_appointments = Appointment.objects.filter(
                professional=professional,
                date=date
            )

            # Se está atualizando um objeto existente, exclua o próprio objeto
            if instance:
                overlapping_appointments = overlapping_appointments.exclude(
                    id=instance.id
                )

            if overlapping_appointments.exists():
                msg = (
                    "Já existe uma consulta marcada para este profissional "
                    "neste horário."
                )
                raise serializers.ValidationError({"date": msg})

        return attrs
