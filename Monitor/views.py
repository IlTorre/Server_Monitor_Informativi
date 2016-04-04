from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

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
            return HttpResponseRedirect(reverse('Monitor:index'))


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