"""Define padroes de URL para learning_logs"""
from django.conf.urls import url
from . import views

urlpatterns = [
    #Pagina inicial
    url(r'^$',views.index, name='index'),
    #Mostra todos os assuntos
    url(r'^topics/$', views.topics, name='topics'),
    #Pagina que mostra o detalhe de um unico assunto
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
]
