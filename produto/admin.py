from django.contrib import admin
from .import models

class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1

class ProtudoAdmin(admin.ModelAdmin):
    inlines = [
        VariacaoInline
    ]

admin.site.register(models.Produto, ProtudoAdmin)
admin.site.register(models.Variacao)



