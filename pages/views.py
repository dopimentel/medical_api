from django.shortcuts import render
from django.views.generic import TemplateView
from professionals.models import Professional
from appointments.models import Appointment
from django.utils import timezone

class HomeView(TemplateView):
    """View da página inicial."""
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obter estatísticas para exibição na página
        context['professionals_count'] = Professional.objects.count()
        context['appointments_count'] = Appointment.objects.count()

        # Obter especialidades únicas
        specialties = set()
        professionals_by_specialty = {}

        for professional in Professional.objects.all():
            if hasattr(professional, 'specialty') and professional.specialty:
                specialty = professional.specialty
                specialties.add(specialty)

                if specialty not in professionals_by_specialty:
                    professionals_by_specialty[specialty] = []
                professionals_by_specialty[specialty].append(professional)

        context['specialties_count'] = len(specialties) if specialties else 0
        context['specialties'] = [
            {
                'name': specialty,
                'count': len(professionals),
                # Limitando a 3 profissionais por especialidade
                'professionals': professionals[:3]
            }
            for specialty, professionals in professionals_by_specialty.items()
        ]

        # Obter próximas consultas
        context['upcoming_appointments'] = Appointment.objects.filter(
            date__gte=timezone.now()
        ).order_by('date')[:5]  # Próximas 5 consultas

        # Data atual para cálculo de tempo restante
        context['current_time'] = timezone.now()

        return context

def home(request):
    # Versão alternativa usando função ao invés de classe
    professionals_count = Professional.objects.count()
    appointments_count = Appointment.objects.count()
    
    # Obter especialidades únicas
    specialties = set()
    for professional in Professional.objects.all():
        if hasattr(professional, 'specialty') and professional.specialty:
            specialties.add(professional.specialty)
    
    specialties_count = len(specialties) if specialties else 0
    
    return render(request, 'pages/home.html', {
        'professionals_count': professionals_count,
        'appointments_count': appointments_count,
        'specialties_count': specialties_count,
    })
