from django.conf.urls import include, url
from . import views

urlpatterns = [
    #url(r'^$',views.mylogin , name='index'),
    url(r'^login/',views.mylogin,name='login'),

]