from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect, HttpResponse, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from Monitor.decorators import controlla_gruppo
from .forms import *
import datetime
from .models import VisualizzataComune, VisualizzataFrazione, VisualizzataMonitor, MonitorUltimaConnessione, MyUser
from Server.settings import TEMPO_ALLERTA
from django.utils import timezone
import json
from .decorators import group_required

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
    try:
        del request.session['comuni_id']
        del request.session['frazioni_id']
        del request.session['monitor_id']
    except KeyError:
        pass
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

    n = [notizia for notizia in Notizia.objects.filter(inserzionista=request.user) if notizia.attiva]

    return render(request, 'Monitor/index.html', {'monitor_in_errore': nmonitor,
                                                  'notizie_non_approvate': nnotizie,
                                                  'notizie': n,
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
    if controlla_gruppo('Inserzionista', request.user):
        if request.method == 'GET':
            return render(request, 'Monitor/inserimento1.html')
        else:
            all_monitor = request.POST['step1']
            if eval(all_monitor):
                form = FormNotizia()
                return render(request, 'Monitor/inserimento_notizia.html', {'form': form})
            else:
                return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))
    else:
        return myindex(request, errore='Solo gli inserzionisti possono inserire le notizie')


@group_required('Inserzionista', login_url='/login')
def nuova_notizia_2(request):
    """
    Gestisce la selezione dei comuni in cui far comparire la notizia
    """
    if request.method == 'GET':
        form = SceltaComuni()
        return render(request, 'Monitor/inserimento2.html', {'form': form})
    else:
            return HttpResponseRedirect(reverse('Monitor:nuova_notzia_da_comune'))


@group_required('Inserzionista', login_url='/login')
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
                comuni.append(Comune.objects.filter(pk=id_com).last())
            request.session['comuni_id'] = comuni_sel
            try:
                del request.session['frazioni_id']
                del request.session['monitor_id']
            except KeyError:
                pass
            return render(request, 'Monitor/inserimento3.html', {'comuni_selezionati': comuni})
        else:
            return myindex(
                request,
                errore="Si è verificato un errore con il form SceltaComuni. Riprova!\nCod Errore: nuova_notizia_3"
            )


@group_required('Inserzionista', login_url='/login')
def nuova_notizia_4(request):
    """
    Gestisce l'inserimento su tutti i monitor dei comuni selezionati o mostra la lista delle frazioni
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))
    else:
        all_comuni = request.POST['comuni_all']

        if eval(all_comuni):
            form = FormNotizia()
            return render(request, 'Monitor/inserimento_notizia.html', {'form': form})

        else:
            com = request.session['comuni_id']
            form = SceltaFrazioni(id_comuni=com)
            return render(request, 'Monitor/inserimento4.html', {'form': form})


@group_required('Inserzionista', login_url='/login')
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
                frazioni.append(Frazione.objects.filter(pk=id_fraz).last())
            request.session['frazioni_id'] = frazioni_sel
            try:
                del request.session['monitor_id']
            except KeyError:
                pass
            return render(request, 'Monitor/inserimento5.html', {'frazioni_selezionate': frazioni})
        else:
            return myindex(
                request,
                errore="Si è verificato un errore con il form SceltaFrazioni. Riprova!\nCod Errore: nuova_notizia_5"
            )


@group_required('Inserzionista', login_url='/login')
def nuova_notizia_6(request):
    """
    Gestisce l'inserimento su tutti i monitor delle frazioni selezionate o mostra la lista dei monitor
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))
    else:
        all_frazioni = request.POST['frazioni_all']

        if eval(all_frazioni):
            form = FormNotizia()
            return render(request, 'Monitor/inserimento_notizia.html', {'form': form})

        else:
            fraz = request.session['frazioni_id']
            form = SceltaMonitor(id_frazioni=fraz)
            return render(request, 'Monitor/inserimento6.html', {'form': form})


@group_required('Inserzionista', login_url='/login')
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
            form = FormNotizia()
            return render(request, 'Monitor/inserimento_notizia.html', {'form': form})
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
    :return: l'oggetto di tipo datetime
    """
    a, m, g = str(data).split('-')
    a = int(a)
    m = int(m)
    g = int(g)
    data = datetime.date(a, m, g)
    hh, mm = str(ora).split(':')
    hh = int(hh)
    mm = int(mm)
    ora = datetime.time(hh, mm)
    data_c = datetime.datetime.combine(data, ora)
    return data_c


@group_required('Inserzionista', login_url='/login')
def finalizza_notizia(request):
    """
    Gestisce il salvataggio della notizia
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))
    else:
        form = FormNotizia(request.POST, request.FILES)
        if form.is_valid():
            notizia = form.save(commit=False)
            data_s = request.POST['data_scadenza']
            if data_s != '':
                notizia.data_scadenza = trasforma_data_ora(data_s, '23:59')
            notizia.inserzionista = request.user
            notizia.save()
            try:
                comuni_id = request.session['comuni_id']
                del request.session['comuni_id']
                try:
                    frazioni_id = request.session['frazioni_id']
                    del request.session['frazioni_id']
                    try:
                        monitor_id = request.session['monitor_id']
                        del request.session['monitor_id']
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

            #invio mail di notifica
            oggetto = "Nuova notizia che richiede approvazione"
            utenti = [utente for utente in MyUser.objects.all() if utente.notifiche_inserzioni_attive()]
            print(utenti)
            for utente in utenti:
                to = utente.email
                content = {'user': utente.username, 'notizia': notizia}

                html_content = render_to_string('Monitor/email/email.html', content)
                text_content = render_to_string('Monitor/email/email.txt', content)

                msg = EmailMultiAlternatives(oggetto, text_content, 'noreply.asteonline@gmail.com', [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

            return myindex(request, ok="Notizia inserita correttamente")
        else:
            return render(request,
                          'Monitor/inserimento_notizia.html',
                          {'form': form,
                           'data_scadenza': request.POST['data_scadenza'],
                           'errore': "I campi Titolo e Descrizione sono obbligatori"}
                          )


@login_required(login_url='/login')
def monitor_in_errore(request):
    """
    Gestisce il recuero e la visualizzazione dei monitor che sono in errore
    """
    in_errore = [monitor for monitor in Monitor.objects.all() if not monitor.funziona()]
    return render(request, 'Monitor/monitor_errore.html', {'tempo': TEMPO_ALLERTA, 'monitor': in_errore})


@login_required(login_url='/login')
def notizie_da_approvare(request):
    """
    Mostra la lista delle notizie da approvare
    """
    notizie = Notizia.objects.filter(approvata=False)
    return render(request, 'Monitor/notizie_da_approvare.html', {'notizie': notizie})


@group_required('Revisore', login_url='/login')
def approva_notizia(request, id_notizia):
    """
    Gestisce la viualizzazione della notizia e la sua attivazione.
    """
    notizia = Notizia.objects.filter(pk=id_notizia).last()
    if request.method == 'GET':
        return render(request, 'Monitor/approva_notizie.html', {'notizia': notizia})
    else:
        if notizia:
            notizia.approvata = not notizia.approvata
            notizia.save()
            return myindex(request, ok='Stato della notizia modificato')
        else:
            return myindex(request, errore='La notizia non è stata trovata.')


def modifica_notizia(request, id_notizia):
    """
    Si occupa della modifica di una notizia
    :param request: la rishiesta http
    :param id_notizia: l'id della notizia da modificare
    :return: il render con l'esito dell' operazione
    """
    notizia = Notizia.objects.filter(pk=id_notizia).last()
    if not notizia:
        return myindex(request, errore='La notizia non è stata trovata.')
    else:
        if controlla_gruppo('Inserzionista', request.user):
            if request.method == 'GET':
                form = FormNotizia(instance=notizia)
                return render(request,
                              'Monitor/modifica_notizia.html',
                              {'form': form})
            else:
                form = FormNotizia(request.POST, request.FILES, instance=notizia)
                if form.is_valid():
                    notizia = form.save(commit=False)
                    data_s = request.POST['data_scadenza']
                    if data_s != '':
                        notizia.data_scadenza = trasforma_data_ora(data_s, '23:59')
                    notizia.approvata = False
                    notizia.inserzionista = request.user
                    notizia.save()
                    return myindex(request, ok='La notizia è stata modificata.')
                else:
                    return render(
                        request,
                        'Monitor/modifica_notizia.html',
                        {'form': form,
                         'errore': "I campi Titolo e Descrizione sono obbligatori."}
                    )
        else:
            return myindex(request, errore='Solo gli inserzionisti possono modificare le notizie')


def monitor_connessione(request, monitor_id=None):
    """
    La classe gestisce la registrazione della connessione in modo da poter identificare
    se un monitor presenta problemi di connessione
    """
    monitor = get_object_or_404(Monitor, pk=monitor_id)
    MonitorUltimaConnessione(monitor=monitor).save()
    return HttpResponse("Aggiornato")


def monitor_ottieni_notizia(request, monitor_id=None):
    """
    Comunicazione delle notizie da mostrare su un monitor
    :param request: la richiesta
    :param monitor_id: l'id identificativo del monitor
    :return: una lista json di notizie oppure un 404 in caso l'id non corrisponda a nessun monitor
    """
    monitor = get_object_or_404(Monitor, pk=monitor_id)

    notizie = [x.notizia for x in VisualizzataComune.objects.filter(comune=monitor.frazione_posizionamento.comune)]
    notizie += [x.notizia for x in VisualizzataFrazione.objects.filter(frazione=monitor.frazione_posizionamento)]
    notizie += [x.notizia for x in VisualizzataMonitor.objects.filter(monitor=monitor)]
    sorted(notizie, key=lambda notizia: notizia.data_scadenza)

    to_js = {notizia.id: [notizia.titolo, notizia.descrizione, str(notizia.immagine), str(notizia.data_scadenza)]
             for notizia in notizie
             if notizia.attiva()}
    return HttpResponse(json.dumps(to_js), content_type="application/json")


@login_required(login_url='/login')
def lista_notizie_attive(request):
    notizie = [notizia for notizia in Notizia.objects.all() if notizia.attiva()]
    return render(request, 'Monitor/notizie_attive.html', {'notizie': notizie})


@login_required(login_url='/login')
def lista_notizie_da_approvare(request):
    notizie = [notizia for notizia in Notizia.objects.all() if not notizia.approvata]
    return render(request, 'Monitor/notizie_non_attive.html', {'notizie': notizie})


@login_required(login_url='/login')
def lista_notizie_scadute(request):
    notizie = [notizia for notizia in Notizia.objects.all() if notizia.data_scadenza < timezone.now()]
    return render(request, 'Monitor/notizie_scadute.html', {'notizie': notizie})


@login_required(login_url='/login')
def lista_monitor(request):
    """
    Gestisce la visualizzazione dell'elenco dei monitor
    :param request: la richiesta html
    :return: il render del template corretto
    """
    monitor = Monitor.objects.all().order_by('frazione_posizionamento','via','nome')
    return render(request,'Monitor/monitor.html',{'monitor':monitor})


def notizie_per_monitor(request, monitor_id):
    monitor = get_object_or_404(Monitor, pk=monitor_id)

    notizie = [x.notizia for x in VisualizzataComune.objects.filter(comune=monitor.frazione_posizionamento.comune)]
    notizie += [x.notizia for x in VisualizzataFrazione.objects.filter(frazione=monitor.frazione_posizionamento)]
    notizie += [x.notizia for x in VisualizzataMonitor.objects.filter(monitor=monitor)]
    sorted(notizie, key=lambda notizia: notizia.data_scadenza)

    return render(request,'Monitor/notizie_per_monitor.html',{'monitor_id':monitor_id, 'notizie':notizie})

