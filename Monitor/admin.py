from django.contrib import admin
from .models import Comune, Frazione, Monitor, MyUser, VisualizzataComune, Notizia

# Register your models here.


class TuttiUtenti(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione degli utenti nel lato amministrativo
    """
    list_display = ('username', 'first_name', 'last_name')
    ordering = ['last_name', 'first_name']


class TuttiComuni(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione dei comuni nel lato amministrativo
    """
    list_display = ('nome',)
    ordering = ['nome']


class TutteFrazioni(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione delle frazioni nel lato amministrativo
    """
    list_display = ('nome', 'comune')
    ordering = ['comune', 'nome']


class TuttiMonitor(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione dei monitor nel lato amministrativo
    """
    list_display = ('nome', 'descrizione', 'via', 'frazione_posizionamento')
    ordering = ['frazione_posizionamento', 'via', 'nome']


class VisualizzatiTuttiMonitor(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione dei monitor nel lato amministrativo
    """
    list_display = ('comune', 'notizia')
    ordering = ['comune']


class TutteNotizie(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione dei monitor nel lato amministrativo
    """
    list_display = ('titolo', 'attiva')
    ordering = ['titolo']

admin.site.register(MyUser, TuttiUtenti)
admin.site.register(Notizia, TutteNotizie)
admin.site.register(Comune, TuttiComuni)
admin.site.register(Frazione, TutteFrazioni)
admin.site.register(Monitor, TuttiMonitor)
admin.site.register(VisualizzataComune, VisualizzatiTuttiMonitor)
