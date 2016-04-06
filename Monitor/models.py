from django.db import models
import os,datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings

def get_nome_immagine_utente(istanza, file):
    """
    Crea il path in cui salvare i le immagini profilo degli utenti
    Per evitare conflitti i file vengono salvati nella cartella
    media/uploaded_files/utenti/{nome_utente}/{data di caricamento}/{ora di caricamento}.estensione
    :param istanza: l'istanza chiamante
    :param file: il file da salvare
    :return: il path
    """
    return os.path.join('uploaded_files',
                        'utenti',
                        str(istanza.username),
                        str(timezone.datetime.date(timezone.now())),
                        str(timezone.datetime.time(timezone.now())).replace(':', '_').replace('.', '_') +
                        os.path.splitext(file)[1]
                        )

class MyUser(AbstractUser):
    """
    Classe che estende la classe user di django per aggiungere campi personalizzati
    """
    foto_profilo = models.ImageField(upload_to=get_nome_immagine_utente,default=settings.NO_PROFILO)

class Comune(models.Model):
    """
    Modello che implementa l'entità comune di appartenenza di un monitor nel db
    """
    nome = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nome

class Frazione(models.Model):
    """
    Modello che implementa l'entità Frazione di appartenenza di un monitor nel db
    """
    nome = models.CharField(max_length=30)
    comune = models.ForeignKey(Comune)

    def __unicode__(self):
        return self.nome

class Monitor(models.Model):
    """
    Entità che implementa l'entità monitor nel db
    """
    nome = models.CharField(max_length=30)
    descrizione = models.CharField(max_length=200)
    via = models.CharField(max_length=30)
    frazione_posizionamento = models.ForeignKey(Frazione)

    def __unicode__(self):
        return self.nome

def get_nome_immagine_notizia(istanza, file):
    """
    Crea il path in cui salvare i le immagini delle notizie
    Per evitare conflitti i file vengono salvati nella cartella
    media/uploaded_files/notizie/{titolonotizia}/{data di caricamento}/{ora di caricamento}.estensione
    :param istanza: l'istanza chiamante
    :param file: il file da salvare
    :return: il path
    """
    return os.path.join('uploaded_files',
                        'notizie',
                        str(istanza.titolo),
                        str(timezone.datetime.date(timezone.now())),
                        str(timezone.datetime.time(timezone.now())).replace(':', '_').replace('.', '_') +
                        os.path.splitext(file)[1]
                        )

class Notizia(models.Model):
    """
    Entità che implementa l'entità notizia nel db
    """
    titolo = models.CharField(max_length=30)
    descrizione = models.CharField(max_length=400)
    immagine = models.ImageField(upload_to=get_nome_immagine_notizia,default=None)
    approvata = models.BooleanField(default=False)
    inserzionista = models.ForeignKey(MyUser)
    data_inserimento = models.DateTimeField(default=timezone.now)
    data_scadenza = models.DateTimeField(default=timezone.now()+datetime.timedelta(days=15))

    def __unicode__(self):
        return self.titolo

    def attiva(self):
        """
        Ritorna se la notizia è attiva e visualizzabile su un monitor
        """
        return self.approvata and (self.data_scadenza>=timezone.now())

class Vis_in_Comune(models.Model):
    """
    Contiene le notizie che si è deciso di visualizzare su tutto il comune
    """
    notizia = models.ForeignKey(Notizia)
    comune = models.ForeignKey(Comune)

class Vis_in_Frazione(models.Model):
    """
    Contiene le notizie che si è deciso di visualizzare su una frazione
    """
    notizia = models.ForeignKey(Notizia)
    comune = models.ForeignKey(Frazione)

class Vis_in_Monitor(models.Model):
    """
    Contiene le notizie che si è deciso di visualizzare su un monitor in particolare
    """
    notizia = models.ForeignKey(Notizia)
    comune = models.ForeignKey(Monitor)

class Ultimo_agg(models.Model):
    """
    Classe che salva l'ultimo aggiornamento che è stato effettuato alle notizie di un determinato monitor
    Si tratta di un dato derivato che però riduce il carico del server al momento dell'aggiornamento dei monitor
    """
    monitor = models.ForeignKey(Monitor).unique
    agg = models.DateTimeField(default=timezone.now)

class Monitor_ultima_connessione(models.Model):
    """
    Classe che tiene traccia dell'ultima connessione effettuata dal monitor.
    Serve per identificare qualche problema alle pensiline
    """
    monitor = models.ForeignKey(Monitor)
    agg = models.DateTimeField(default=timezone.now)

    def funziona(self):
        """
        Ritorna lo stato di funzionamento del monitor
        """
        return self.agg>=timezone.now()-datetime.timedelta(hours=settings.TEMPO_ALLERTA)