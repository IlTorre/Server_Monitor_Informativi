from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
import datetime
from .models import VisualizzataComune, VisualizzataFrazione, VisualizzataMonitor

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
def myindex(request):
    """
    Gestisce la visualizzazione della home page
    """

    return render(request, 'Monitor/base.html')


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
            print('Errore form non valido 3')


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
            print("form non valido 5")


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
            print("form non valido 7")


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
            try:
                comuni_id = request.session['comuni_id']
                try:
                    frazioni_id = request.session['frazioni_id']
                    try:
                        monitor_id = request.session['monitor_id']
                        """
                        Inserimento notizia per monitor
                        """
                        pass

                    except KeyError:
                        """
                        Inserimento per frazioni
                        """
                        pass

                except KeyError:
                    """
                    Inserimento notizia per comune
                    """
                    pass

            except KeyError:
                """
                Inserimento notizia su tutti i monitor disponibili
                """
                notizia = immagine.save(commit=False)
                notizia.titolo = request.POST['titolo']
                notizia.descrizione = request.POST['descrizione']

                data_s = request.POST['data_scadenza']
                if data_s != '':
                    a, m, g = str(data_s).split('-')
                    a = int(a)
                    m = int(m)
                    g = int(g)
                    data_s = datetime.date(a, m, g)
                    ora_s = datetime.time(23, 59)
                    data = datetime.datetime.combine(data_s, ora_s)
                    notizia.data_scadenza = data

                notizia.inserzionista = request.user
                notizia.save()
                comuni = Comune.objects.all()
                for comune in comuni:
                    VisualizzataComune(comune=comune, notizia=notizia).save()
                return HttpResponseRedirect(reverse('Monitor:index'))

        else:
            print("errore form finalizza")

