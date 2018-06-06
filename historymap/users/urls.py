from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .signup import signup
urlpatterns=[
        url(r'^login/$', auth_views.login, name='login'),
        url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
        url(r'^signup/$', signup,name='signup'),
        
]
