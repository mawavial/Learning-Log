"""Define padroes de URL para users"""

from django.conf.urls import url
from django.contrib.auth.views import login

from . import views
#ll_env - pythonpython
urlpatterns = [
    #pagina de login
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login'),
    #pagina de logout
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$',views.register, name='register'),
    
]