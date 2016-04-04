from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$',views.myindex, name='index'),
    url(r'^login/',views.mylogin, name='login'),
    url(r'^logout/', views.mylogout, name='logout'),
    url(r'^inserisci/$', views.nuova_notizia_1, name='inserimento_step1'),
    url(r'^inserisci/comune', views.nuova_notizia_2, name='nuova_notizia_da_comune'),

]