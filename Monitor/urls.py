from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.myindex, name='index'),
    url(r'^login/', views.mylogin, name='login'),
    url(r'^logout/', views.mylogout, name='logout'),
    url(r'^inserisci/AllMonitor$', views.nuova_notizia_1, name='inserimento_step1'),
    url(r'^inserisci/comune', views.nuova_notizia_2, name='nuova_notizia_da_comune'),
    url(r'^inserisci/AllComune', views.nuova_notizia_3, name='inserimento_step3'),
    url(r'^inserisci/frazioni', views.nuova_notizia_4, name='inserimento_step4'),
    url(r'^inserisci/AllFrazioni', views.nuova_notizia_5, name='inserimento_step5'),
    url(r'^inserisci/monitor', views.nuova_notizia_6, name='inserimento_step6'),
    url(r'^inserisci/notizia', views.nuova_notizia_7, name='inserimento_step7'),
    url(r'^inserisci/FineInserimento', views.finalizza_notizia, name='finalizza_notizia'),
    url(r'^statoMonitor', views.monitor_in_errore, name='stato_monitor'),
    url(r'^NotizieDaApprovare', views.notizie_da_approvare, name='notizie_da_approvare'),
    url(r'^approva/(?P<id_notizia>[0-9]+)$', views.approva_notizia, name='approva_notizia'),
    url(r'^modifica/(?P<id_notizia>[0-9]+)$', views.modifica_notizia, name='modifica_notizia'),
    url(r'^monitor/sonovivo/(?P<monitor_id>[0-9]+)$', views.monitor_connessione, name='monitor_vivo'),
    url(r'^monitor/notizie/(?P<monitor_id>[0-9]+)$', views.monitor_ottieni_notizia, name='monitor_ottieni_notizia'),
    url(r'^notizie/attive/$', views.lista_notizie_attive, name='lista_attive'),
    url(r'^notizie/non_attive/$', views.lista_notizie_da_approvare, name='lista_non_attive'),
    url(r'^notizie/scadute/$', views.lista_notizie_scadute, name='lista_scadute'),
    url(r'^visualizza/monitor/$', views.lista_monitor, name='lista_monitor'),
    url(r'^visualizza/monitor/(?P<monitor_id>[0-9]+)$', views.notizie_per_monitor, name='notizie_monitor'),

]
