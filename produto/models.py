from django.db import models
from PIL import Image
import os
from django.conf import settings

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m/')
    slug = models.SlugField(unique=True)
    preco = models.FloatField(default=0)
    preco_promocao = models.FloatField(default=0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variação'),
            ('S', 'Simples'),
        )
    )

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.image

        if original_width <= new_width:
            img.pil.close()
            return

        new_height = round((new_width * original_height) / original_width)
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50,
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

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
