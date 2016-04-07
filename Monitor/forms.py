from django import forms
from .models import Comune, Frazione, Monitor, Notizia


def ottieni_comuni():
    """
    Seleziona i comuni e le formatta per essere passati come scelta al form
    """
    comuni = Comune.objects.all()
    choices = []
    for comune in comuni:
        choices.append((comune.id, comune.nome))
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
    comuni = []
    for x in id_comuni:
        y = Comune.objects.filter(id=x).last()
        comuni.append(y)
    frazioni = []
    for comune in comuni:
        y = Frazione.objects.filter(comune=comune)
        frazioni += y
    choices = []

    for frazione in frazioni:
        choices.append((frazione.id, frazione.nome + " - " + frazione.comune.nome))
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
    frazioni = []
    for x in id_frazioni:
        y = Frazione.objects.filter(id=x).last
        frazioni.append(y)
    monitor = []
    for frazione in frazioni:
        y = Monitor.objects.filter(frazione_posizionamento=frazione)
        monitor += y
    choices = []

    for m in monitor:
        choices.append((m.id, m.nome + " - " + m.frazione_posizionamento.nome))
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
    class Meta:
        """
        Classe delle metainformazioni che specifica il modello da utilizzare e i campi.
        """
        model = Notizia
        fields = ['foto']
