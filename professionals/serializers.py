from rest_framework import serializers
from .models import Professional


class ProfessionalSerializer(serializers.ModelSerializer):
    """
    Serializer for the Professional model.
    """

    class Meta:
        model = Professional
        fields = [
            "id",
            "preferred_name",
            "profession",
            "address",
            "contact",
        ]
        
    def validate_contact(self, value):
        """
        Validação adicional para o campo contact.
        """
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError(
                "O contato deve ser um número telefônico com 11 dígitos."
            )
        return value
