import factory
from django.contrib.auth import get_user_model
from professionals.models import Professional
from appointments.models import Appointment

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

class ProfessionalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Professional
    
    user = factory.SubFactory(UserFactory)
    crm = factory.Sequence(lambda n: f"CRM{n:06d}")
    specialty = factory.Faker("job")

class AppointmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Appointment
    
    professional = factory.SubFactory(ProfessionalFactory)
    patient_name = factory.Faker("name")
    date_time = factory.Faker("future_datetime")
    status = "scheduled"