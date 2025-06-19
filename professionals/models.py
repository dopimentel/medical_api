from django.db import models
from django.core.validators import RegexValidator


class Professional(models.Model):
    """
    Model representing health professionals.
    """

    preferred_name = models.CharField("Nome Social", max_length=255)
    profession = models.CharField("Profissão", max_length=100)
    specialty = models.CharField("Especialidade", max_length=100, blank=True, null=True)
    address = models.TextField("Endereço")
    phone_regex = RegexValidator(
        regex=r'^\d{11}$',
        message="The phone number must contain 11 numeric digits."
    )
    contact = models.CharField("Contato", max_length=11, validators=[phone_regex])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profissional"
        verbose_name_plural = "Profissionais"
        ordering = ["preferred_name"]

    def __str__(self):
        return f"{self.preferred_name} - {self.profession}"
