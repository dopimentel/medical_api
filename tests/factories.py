import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from professionals.models import Professional
from appointments.models import Appointment

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name", locale="pt_BR")
    last_name = factory.Faker("last_name", locale="pt_BR")
    is_active = True


class ProfessionalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Professional
    
    preferred_name = factory.Faker("name", locale="pt_BR")
    profession = factory.Faker("job", locale="pt_BR")
    address = factory.Faker("address", locale="pt_BR")
    contact = factory.Sequence(lambda n: f"119999{n:05d}")


class AppointmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Appointment
    
    professional = factory.SubFactory(ProfessionalFactory)
    date = factory.LazyFunction(
        lambda: timezone.now() + timedelta(days=1, hours=2)
    )