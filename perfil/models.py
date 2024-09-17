from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re


class Perfil(models.Model):
    nome = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    numero_telefone = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.nome.first_name} {self.nome.last_name}'
    
    def clean(self):
        error_messages = {}

        if re.search(r'[^0-9]', self.numero_telefone) or len(self.numero_telefone) <10:
            error_messages['numero_telefone'] = 'Digite um número de celular válido'

        if error_messages:
            raise ValidationError(error_messages)

    # error_messages['campo'] = 'Message'
    
    # def clean(self):
    #     raise ValidationError({
    #         'idade': 'Blablablabla'
    #     })
    # O ValidationError é utilizado para levantar uma execeção em algum campo.
    # Nós escolhesmos o campo. Ex. idade, e colocamos a execeção que queremos exibir,
    # nesse caso foi Blablablabla
    # O método clean é utilizado para fazer a validação de algum campo

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'