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
            "name",
            "profession",
            "address",
            "contact",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
