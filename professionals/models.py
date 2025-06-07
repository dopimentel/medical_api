from django.db import models


class Professional(models.Model):
    """
    Model representing health professionals.
    """

    name = models.CharField("Nome Social", max_length=255)
    profession = models.CharField("Profissão", max_length=100)
    address = models.TextField("Endereço")
    contact = models.CharField("Contato", max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profissional"
        verbose_name_plural = "Profissionais"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.profession}"
