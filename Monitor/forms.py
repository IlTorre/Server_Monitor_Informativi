from django import forms
from .models import Comune, Frazione, Monitor, Notizia
from Server import settings


def ottieni_comuni():
    """
    Seleziona i comuni e le formatta per essere passati come scelta al form
    """
    choices = [(comune.id, comune.nome)for comune in Comune.objects.all()]
    return choices


class SceltaComuni(forms.Form):
    """
    Form per la scelta multipla dei comuni
    """
    comuni_s = forms.MultipleChoiceField(
        choices=ottieni_comuni(),
        widget=forms.CheckboxSelectMultiple,
        label='',
    )


def ottieni_frazioni(id_comuni):
    comuni = [Comune.objects.filter(pk=id_comune) for id_comune in id_comuni]
    frazioni = []
    for comune in comuni:
        y = Frazione.objects.filter(comune=comune)
        frazioni += y
    choices = [(frazione.id, frazione.nome + " - " + frazione.comune.nome) for frazione in frazioni]
    return choices


class SceltaFrazioni (forms.Form):
    """
    Gestisce la creazione del form per la scelta delle frazioni
    """
    frazioni_s = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='',
        )

    def __init__(self, *args, **kwargs):
        id_comuni = kwargs.pop('id_comuni', None)
        super(SceltaFrazioni, self).__init__(*args, **kwargs)
        if id_comuni:
            self.fields['frazioni_s'].choices = ottieni_frazioni(id_comuni)


def ottieni_monitor(id_frazioni):
    """
    Funzione per la selezione dei monitor appartenenti a una serie di frazioni
    :param id_frazioni: una lista di id di frazioni
    :return: una lista di monitor associati
    """
    frazioni = [Frazione.objects.filter(pk=id_frazione) for id_frazione in id_frazioni]
    monitor = []
    for frazione in frazioni:
        y = Monitor.objects.filter(frazione_posizionamento=frazione)
        monitor += y
    choices = [(m.id, m.nome + " - " + m.frazione_posizionamento.nome) for m in monitor]
    return choices


class SceltaMonitor (forms.Form):
    """
    Gestisce la creazione del form per la scelta dei monitor
    """
    monitor_s = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='',
        )

    def __init__(self, *args, **kwargs):
        id_frazioni = kwargs.pop('id_frazioni', None)
        super(SceltaMonitor, self).__init__(*args, **kwargs)
        if id_frazioni:
            self.fields['monitor_s'].choices = ottieni_monitor(id_frazioni)


class CaricaFotoNotizia (forms.ModelForm):
    """
    Classe che implementa il form di caricamento della foto delle notizie
    """
    titolo = forms.CharField(required=True, max_length=settings.MAX_LUN_TITOLO)
    descrizione = forms.CharField(widget=forms.Textarea,required=True, max_length=settings.MAX_LUN_DESCRIZIONE)
    immagine = forms.ImageField(required=False)

    class Meta:
        """
        Classe delle metainformazioni che specifica il modello da utilizzare e i campi.
        """
        model = Notizia
        fields = ['titolo','descrizione','immagine']
