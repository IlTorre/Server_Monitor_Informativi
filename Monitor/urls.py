from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$',views.myindex, name='index'),
    url(r'^login/',views.mylogin, name='login'),
    url(r'^logout/', views.mylogout, name='logout'),

]