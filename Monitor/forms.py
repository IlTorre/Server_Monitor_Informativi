from django import forms
from .models import Comune

def ottieni_comuni():
    comuni=Comune.objects.order_by('nome')
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