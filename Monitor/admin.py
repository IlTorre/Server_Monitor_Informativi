from django.contrib import admin
from .models import Comune, Frazione, Monitor

# Register your models here.

class TuttiComuni(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione deli comuni nel lato amministrativo
    """
    list_display = ('nome',)
    #ordering = ['nome']


class TutteFrazioni(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione deli comuni nel lato amministrativo
    """
    list_display = ('nome','comune')
    #ordering = ['comune','nome']


class TuttiMonitor(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione deli comuni nel lato amministrativo
    """
    list_display = ('nome','via','descrizione')
    #ordering = ['frazione','via','nome']

admin.site.register(Comune, TuttiComuni)
admin.site.register(Frazione, TutteFrazioni)
admin.site.register(Monitor, TuttiMonitor)