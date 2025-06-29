# Generated by Django 5.2.2 on 2025-06-08 06:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0003_alter_professional_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professional',
            name='contact',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='The phone number must contain 11 numeric digits.', regex='^\\d{11}$')], verbose_name='Contato'),
        ),
    ]
