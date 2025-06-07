from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Professional
from .serializers import ProfessionalSerializer


class ProfessionalViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualização e edição de profissionais.

    list:
    Retorna uma lista de todos os profissionais.

    create:
    Cria um novo profissional.

    retrieve:
    Retorna um profissional específico.

    update:
    Atualiza um profissional específico.

    partial_update:
    Atualiza parcialmente um profissional específico.

    destroy:
    Remove um profissional específico.
    """

    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["profession"]
    search_fields = ["name", "profession", "address", "contact"]
    ordering_fields = ["name", "profession", "created_at"]
    ordering = ["name"]
