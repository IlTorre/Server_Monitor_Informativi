from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from django import forms

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
                return render(request, 'Monitor/login.html', {'messaggio':'Account inattivo!'})
        else:
            return render(request, 'Monitor/login.html', {'messaggio': 'Nome utente o password errati, riprova!'})
    else:
        if request.user.is_anonymous():
            return render(request, 'Monitor/login.html')
        else:
            return HttpResponseRedirect(reverse('Monitor:index'), {'utente':request.user})


@login_required(login_url='/login')
def myindex (request):
    """
    Gestisce la visualizzazione della home page
    """

    return render(request,'Monitor/base.html', {'utente':request.user})


@login_required(login_url='/login')
def mylogout (request):
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
        return render(request, 'Monitor/inserimento1.html', {'utente':request.user})
    else:
        all_monitor = request.POST['step1']
        if eval(all_monitor):
            pass
        else:
            return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))


@login_required(login_url='/login')
def nuova_notizia_2(request):
    """
    Gestisce la selezione dei comuni in cui far comparire la notizia
    """
    if request.method == 'GET':
        form = SceltaComuni()
        return render(request, 'Monitor/inserimento2.html', {'utente': request.user,'form':form})
    else:
            return HttpResponseRedirect(reverse('Monitor:nuova_notzia_da_comune'))

@login_required(login_url='/login')
def nuova_notizia_3(request):
    """
    Gestisce l'inserimento della notizia su tutti i monitor di un comune o solo su una parte di essi
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))
    else:
        form = SceltaComuni(request.POST)
        if form.is_valid():
            comuni_sel = form.cleaned_data.get('comuni_s')
            comuni = []
            for id in comuni_sel:
                comuni.append(Comune.objects.filter(id=id).last())
            request.session['comuni_id']=comuni_sel
            return render(request, 'Monitor/inserimento3.html', {'utente': request.user, 'comuni_selezionati':comuni})
        else:
            print('Errore form non valido')


@login_required(login_url='/login')
def nuova_notizia_4(request):
    """
    Gestisce l'inserimento la selezione delle frazioni
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))
    else:
        all_comuni = request.POST['comuni_all']

        if eval(all_comuni):
            pass

        else:
            com=request.session['comuni_id']
            form = SceltaFrazioni(id_frazioni=com)
            print(type(form))
            return render(request, 'Monitor/inserimento4.html', {'utente': request.user, 'form': form})


@login_required(login_url='/login')
def nuova_notizia_5(request):
    """
    Gestisce l'inserimento della notizia su tutti i monitor di un comune o solo su una parte di essi
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('Monitor:nuova_notizia_da_comune'))
    else:
        form = SceltaComuni(request.POST)
        if form.is_valid():
            comuni_sel = form.cleaned_data.get('comuni_s')
            comuni = []
            for id in comuni_sel:
                comuni.append(Comune.objects.filter(id=id).last())
            request.session['comuni_id']=comuni_sel
            return render(request, 'Monitor/inserimento3.html', {'utente': request.user, 'comuni_selezionati':comuni})