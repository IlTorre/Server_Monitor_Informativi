from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
import datetime
from .models import VisualizzataComune, VisualizzataFrazione, VisualizzataMonitor
from Server.settings import TEMPO_ALLERTA

# Create your views here.


def mylogin(request):
    """
    Gestisce il login:
    In caso di get
        effettua il render del templates se l'utente che effettua la richiesta non è autenticato, in caso contrario
        redireziona al profilo
    In caso di post
        Autentica l'utente con le opportune verifiche
    :param request: la richiesta
    :return: il render del templates corretto
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Monitor:index'))
            else:
                return render(request, 'Monitor/login.html', {'messaggio': 'Account inattivo!'})
        else:
            return render(request, 'Monitor/login.html', {'messaggio': 'Nome utente o password errati, riprova!'})
    else:
        if request.user.is_anonymous():
            return render(request, 'Monitor/login.html')
        else:
            return HttpResponseRedirect(reverse('Monitor:index'))


@login_required(login_url='/login')
def myindex(request, ok=None, errore=None):
    """
    Gestisce la visualizzazione della home page
    """
    monitor = Monitor.objects.all()
    nmonitor = 0
    for x in monitor:
        if not x.funziona():
            nmonitor += 1
    notizie = Notizia.objects.all()
    nnotizie = 0
    for notizia in notizie:
        if not notizia.approvata:
            nnotizie += 1

    return render(request, 'Monitor/index.html', {'monitor_in_errore': nmonitor,
                                                  'notizie_non_approvate': nnotizie,
                                                  'ok': ok,
                                                  'errore': errore})


@login_required(login_url='/login')
def mylogout(request):
    """
    Permette all'utente che effettua la richiesta di uscire dalla sessione
    :param request: la richiesta
    :return: il render alla pagina di login
    """
    logout(request)
    return HttpResponseRedirect(reverse('Monitor:login'))


@login_required(login_url='/login')
def nuova_notizia_1(request):
    """
    Gestisce l'inserimento della notizia su tutti i monitor o solo su una parte di essi
    """
    if request.method == 'GET':
        return render(request, 'Monitor/inserimento1.html')
    else:
        all_monitor = request.POST['step1']
        if eval(all_monitor):
            immagine = CaricaFotoNotizia()
            return render(request, 'Monitor/inserimento_notizia.html', {'immagine': immagine})
        else:
            return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))


@login_required(login_url='/login')
def nuova_notizia_2(request):
    """
    Gestisce la selezione dei comuni in cui far comparire la notizia
    """
    if request.method == 'GET':
        form = SceltaComuni()
        return render(request, 'Monitor/inserimento2.html', {'form': form})
    else:
            return HttpResponseRedirect(reverse('Monitor:nuova_notzia_da_comune'))


@login_required(login_url='/login')
def nuova_notizia_3(request):
    """
    Gestisce la selezione dei comuni e gestisce la richiesta di inserimento su tutti i monitor dei comuni selezionati
    o se solo su una parte.
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))
    else:
        form = SceltaComuni(request.POST)
        if form.is_valid():
            comuni_sel = form.cleaned_data.get('comuni_s')
            comuni = []
            for id_com in comuni_sel:
                comuni.append(Comune.objects.filter(id=id_com).last())
            request.session['comuni_id'] = comuni_sel
            return render(request, 'Monitor/inserimento3.html', {'comuni_selezionati': comuni})
        else:
            return myindex(
                request,
                errore="Si è verificato un errore con il form SceltaComuni. Riprova!\nCod Errore: nuova_notizia_3"
            )


@login_required(login_url='/login')
def nuova_notizia_4(request):
    """
    Gestisce l'inserimento su tutti i monitor dei comuni selezionati o mostra la lista delle frazioni
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))
    else:
        all_comuni = request.POST['comuni_all']

        if eval(all_comuni):
            return render(request, 'Monitor/inserimento_notizia.html')

        else:
            com = request.session['comuni_id']
            form = SceltaFrazioni(id_comuni=com)
            return render(request, 'Monitor/inserimento4.html', {'form': form})


@login_required(login_url='/login')
def nuova_notizia_5(request):
    """
    Gestisce la selezione delle frazioni e gestisce la richiesta di inserimento su tutti i monitor delle frazioni
    selezionate o se solo su una parte.
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))
    else:
        com = request.session['comuni_id']
        form = SceltaFrazioni(request.POST, id_comuni=com)
        if form.is_valid():
            frazioni_sel = form.cleaned_data.get('frazioni_s')
            frazioni = []
            for id_fraz in frazioni_sel:
                frazioni.append(Frazione.objects.filter(id=id_fraz).last())
            request.session['frazioni_id'] = frazioni_sel
            return render(request, 'Monitor/inserimento5.html', {'frazioni_selezionate': frazioni})
        else:
            return myindex(
                request,
                errore="Si è verificato un errore con il form SceltaFrazioni. Riprova!\nCod Errore: nuova_notizia_5"
            )


@login_required(login_url='/login')
def nuova_notizia_6(request):
    """
    Gestisce l'inserimento su tutti i monitor delle frazioni selezionate o mostra la lista dei monitor
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))
    else:
        all_frazioni = request.POST['frazioni_all']

        if eval(all_frazioni):
            return render(request, 'Monitor/inserimento_notizia.html')

        else:
            fraz = request.session['frazioni_id']
            form = SceltaMonitor(id_frazioni=fraz)
            return render(request, 'Monitor/inserimento6.html', {'form': form})


@login_required(login_url='/login')
def nuova_notizia_7(request):
    """
    Gestisce la selezione dei monitor e gestisce la richiesta di inserimento su i monitor selezionati
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))
    else:
        fraz = request.session['frazioni_id']
        form = SceltaMonitor(request.POST, id_frazioni=fraz)
        if form.is_valid():
            monitor_sel = form.cleaned_data.get('monitor_s')
            request.session['monitor_id'] = monitor_sel
            return render(request, 'Monitor/inserimento_notizia.html')
        else:
            return myindex(
                request,
                errore="Si è verificato un errore con il form SceltaMonitor. Riprova!\nCod Errore: nuova_notizia_7"
            )


def trasforma_data_ora(data, ora):
    """
    Trasforma una data e un ora in un datetime necessario alla memorizzazione nel db
    :param data: una data espressa nel formato yyyy-mm-gg
    :param ora: un orario espresso nel formato hh:mm
    :return
    """
    a, m, g = str(data).split('-')
    a = int(a)
    m = int(m)
    g = int(g)
    data = datetime.date(a, m, g)
    hh, mm = str(ora).split(':')
    ora = datetime.time(hh, mm)
    data_c = datetime.datetime.combine(data, ora)
    return data_c


@login_required(login_url='/login')
def finalizza_notizia(request):
    """
    Gestisce il salvataggio della notizia
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))
    else:
        immagine = CaricaFotoNotizia(request.POST, request.FILES)
        if immagine.is_valid():
            notizia = immagine.save(commit=False)
            notizia.titolo = request.POST['titolo']
            notizia.descrizione = request.POST['descrizione']
            data_s = request.POST['data_scadenza']
            if data_s != '':
                notizia.data_scadenza = trasforma_data_ora(data_s, '23:59')
            notizia.inserzionista = request.user
            notizia.save()
            try:
                comuni_id = request.session['comuni_id']
                try:
                    frazioni_id = request.session['frazioni_id']
                    try:
                        monitor_id = request.session['monitor_id']
                        """
                        Inserimento notizia per monitor
                        """
                        monitor = []
                        for m_id in monitor_id:
                            monitor.append(Monitor.objects.filter(id=m_id).last())
                        for x in monitor:
                            VisualizzataMonitor(monitor=x, notizia=notizia).save()

                    except KeyError:
                        """
                        Inserimento per frazioni
                        """
                        frazioni = []
                        for id_frazione in frazioni_id:
                            frazioni.append(Frazione.objects.filter(id=id_frazione).last())
                        for frazione in frazioni:
                            VisualizzataFrazione(frazione=frazione, notizia=notizia).save()

                except KeyError:
                    """
                    Inserimento notizia per comune
                    """
                    comuni = []
                    for id_comune in comuni_id:
                        comuni.append(Comune.objects.filter(id=id_comune).last())
                    for comune in comuni:
                        VisualizzataComune(comune=comune, notizia=notizia).save()

            except KeyError:
                """
                Inserimento notizia su tutti i monitor disponibili: in tutti i comuni
                """
                comuni = Comune.objects.all()
                for comune in comuni:
                    VisualizzataComune(comune=comune, notizia=notizia).save()

            return HttpResponseRedirect(reverse('Monitor:index'))
        else:
            return myindex(
                request,
                errore="Si è verificato un errore con il form CaricaFotoNotizia. Riprova\nCod Errore: finalizza_notizia"
            )


@login_required(login_url='/login')
def monitor_in_errore(request):
    """
    Gestisce il recuero e la visualizzazione dei monitor che sono in errore
    """
    monitor = Monitor.objects.all()
    in_errore = []
    for x in monitor:
        if not x.funziona():
            in_errore.append(x)
    return render(request, 'Monitor/monitor_errore.html', {'tempo':TEMPO_ALLERTA, 'monitor': in_errore})


@login_required(login_url='/login')
def notizie_da_approvare(request):
    """
    Mostra la lista delle notizie da approvare
    """
    notizie = Notizia.objects.filter(approvata=False)
    return render(request, 'Monitor/notizie_da_approvare.html', {'notizie': notizie})


@login_required(login_url='/login')
def approva_notizia(request, id_notizia):
    """
    Gestisce la viualizzazione della notizia e la sua attivazione.

    """
    if request.user.has_perm('Monitor.change_Notizia') and not request.user.has_perm('Monitor.add_Notizia'):
        notizia = Notizia.objects.filter(id=id_notizia).last()
        if request.method == 'GET':
            return render(request,'Monitor/approva_notizie.html', {'notizia': notizia})
        else:
            if notizia:
                notizia.approvata = True
                notizia.save()
                return myindex(request, ok='La notizia è ora stata attivata. A breve potrà comparire sui monitor.')
            else:
                return myindex(request, errore='La notizia non è stata trovata.')
    else:
            return myindex(request,errore='Solo i revisori possono approvare le notizie')