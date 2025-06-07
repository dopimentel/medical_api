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
