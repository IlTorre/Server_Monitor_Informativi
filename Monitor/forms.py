from django import forms
from .models import Comune, Frazione

def ottieni_comuni():
    comuni=Comune.objects.all()
    choices=[]
    for comune in comuni:
        choices.append((comune.id,comune.nome))
    return choices


class SceltaComuni(forms.Form):
    """
    Form per la scelta multipla dei comuni
    """
    comuni_s = forms.MultipleChoiceField(
        choices = ottieni_comuni(),
        widget = forms.CheckboxSelectMultiple,
        label='',
    )

def ottieni_frazioni(id_frazioni):
    comuni = []
    for x in id_frazioni:
        y = Comune.objects.filter(id=x).last()
        comuni.append(y)
    frazioni = []
    for comune in comuni:
        y = Frazione.objects.filter(comune=comune)
        frazioni += y
    choices = []

    for frazione in frazioni:
        choices.append((frazione.id, frazione.nome))
    return choices


class SceltaFrazioni (forms.Form):
    """

    """
    frazioni_s = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='',
        )

    def __init__(self, *args, **kwargs):
        id_frazioni = kwargs.pop('id_frazioni')
        print(id_frazioni)
        super(SceltaFrazioni, self).__init__(*args, **kwargs)
        self.fields['frazioni_s'].choices = ottieni_frazioni(id_frazioni)





