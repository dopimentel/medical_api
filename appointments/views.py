from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    DateTimeFilter,
    DateFilter
)
from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentFilterSet(FilterSet):
    """
    FilterSet personalizado para Appointment.
    """

    start_date = DateTimeFilter(field_name="date", lookup_expr="gte")
    end_date = DateTimeFilter(field_name="date", lookup_expr="lte")
    date = DateFilter(field_name="date", lookup_expr="date")

    class Meta:
        model = Appointment
        fields = {
            "professional": ["exact"],
        }


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualização e edição de consultas.
    """

    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AppointmentFilterSet
    ordering_fields = ["date", "created_at"]
    ordering = ["-date"]

    def get_queryset(self):
        """
        Retorna consultas com prefetch dos dados do profissional
        """
        return Appointment.objects.all().select_related("professional")
