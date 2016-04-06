from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$',views.myindex, name='index'),
    url(r'^login/',views.mylogin, name='login'),
    url(r'^logout/', views.mylogout, name='logout'),
    url(r'^inserisci/AllMonitor$', views.nuova_notizia_1, name='inserimento_step1'),
    url(r'^inserisci/comune', views.nuova_notizia_2, name='nuova_notizia_da_comune'),
    url(r'^inserisci/AllComune', views.nuova_notizia_3, name='inserimento_step3'),
    url(r'^inserisci/frazioni', views.nuova_notizia_4, name='inserimento_step4'),
    url(r'^inserisci/frazioni2', views.nuova_notizia_4, name='inserimento_step5'),


]