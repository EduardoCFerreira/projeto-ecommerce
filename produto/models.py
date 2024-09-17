from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m/')
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco = models.FloatField(default=0, verbose_name='Preço')
    preco_promocao = models.FloatField(default=0, verbose_name='Preço de promoção')
                                        # Verbose name é utilizado para mudar o nome da tabela
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variação'),
            ('S', 'Simples'),
        )
    )

    def get_preco_formatado(self):
        return f'R$ {self.preco:.2f}'.replace('.', ',')
    get_preco_formatado.short_description = "Preco"

    def get_preco_promocao_formatado(self):
        return f'R$ {self.preco_promocao:.2f}'.replace('.', ',')
    get_preco_promocao_formatado.short_description = "Preco de promoção"
    # Essa função que foi criada retorna o próprio valor, onde é utilizada um fStr para
    # mudar o preco para ponto flutuante e chama a função replace para mudar os . para ,

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
#   ^^^^^^^^^^^^^^^^^^^^ <-- Todo esse metodo é utilizado para retornar o nome no banco de dados

class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
                                                        # ^^^^^^ <-- Quando deletar a variação,
                                                        #  O produto é apagado tbm.
    nome = models.CharField(max_length=200)
    preco= models.FloatField()
    preco_promocao = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome
#   ^^^^^^^^^^^^^^^^^^^^ <-- Todo esse metodo é utilizado para retornar o nome no banco de dados
    class Meta:
        verbose_name = "Variação"
        verbose_name_plural = "Variações"
