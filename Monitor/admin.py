from django.contrib import admin
from .models import Comune, Frazione, Monitor, MyUser, VisualizzataComune, Notizia, MonitorUltimaConnessione
from Server.settings import DEBUG

# Register your models here.


class TuttiUtenti(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione degli utenti nel lato amministrativo
    """
    list_display = ('username', 'first_name', 'last_name')
    ordering = ['last_name', 'first_name']

    fieldsets = [
        ('Dati Anagrafici', {'fields': ['first_name', 'last_name']}),
        ('Informazioni aggiuntive', {'fields': ['username', 'email', 'password']}),
        ('Ruolo ricoperto', {'fields': ['groups', ]}),
    ]

    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"


class TuttiComuni(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione dei comuni nel lato amministrativo
    """
    list_display = ('nome',)
    ordering = ['nome']

    class Meta:
        verbose_name = "Comune"
        verbose_name_plural = "Comuni"


class TutteFrazioni(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione delle frazioni nel lato amministrativo
    """
    list_display = ('nome', 'comune')
    ordering = ['comune', 'nome']

    class Meta:
        verbose_name = "Frazione"
        verbose_name_plural = "Frazioni"


class TuttiMonitor(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione dei monitor nel lato amministrativo
    """
    list_display = ('nome', 'descrizione', 'via', 'frazione_posizionamento')
    ordering = ['frazione_posizionamento', 'via', 'nome']

    class Meta:
        verbose_name = "Monitor"
        verbose_name_plural = "Monitor"


class VisualizzatiTuttiMonitor(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione delle notizie isualizzate su un intero comune nel lato amministrativo
    """
    list_display = ('comune', 'notizia')
    ordering = ['notizia', 'comune']

    class Meta:
        verbose_name = "Notizia visualizzata su un intero comune"
        verbose_name_plural = "Notizie visualizzate su un intero comune"


class TutteNotizie(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione delle notizie nel lato amministrativo
    """
    list_display = ('titolo', 'attiva')
    ordering = ['titolo']

    class Meta:
        verbose_name = "Notizia"
        verbose_name_plural = "Notizie"


class TutteCon(admin.ModelAdmin):
    """
    Classe che definisce la visualizzazione dei monitor nel lato amministrativo
    """
    list_display = ('monitor', 'agg')

admin.site.register(MyUser, TuttiUtenti)
admin.site.register(Comune, TuttiComuni)
admin.site.register(Frazione, TutteFrazioni)
admin.site.register(Monitor, TuttiMonitor)

if DEBUG:
    admin.site.register(Notizia, TutteNotizie)
    admin.site.register(VisualizzataComune, VisualizzatiTuttiMonitor)
    admin.site.register(MonitorUltimaConnessione, TutteCon)
