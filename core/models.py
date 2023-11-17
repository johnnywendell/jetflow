from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser

class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        'criado em',
        auto_now_add=True,
        auto_now=False
    )
    modified = models.DateTimeField(
        'modificado em',
        auto_now_add=False,
        auto_now=True
    )
    class Meta:
        abstract = True

class DialogoComportamental(models.Model):
    data = models.DateField('data')
    nome = models.CharField('nome', max_length=30)
    local = models.CharField('local', max_length=30)
    relato = models.CharField('relato', max_length=30)

class DialogoForm(forms.ModelForm):
    class Meta:
        model = DialogoComportamental
        fields = '__all__'