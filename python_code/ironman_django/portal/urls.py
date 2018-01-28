from django.conf.urls import url

from . import views

urlpatterns = [
    # '/'
    url(r'^$', views.index, name='index'),
    # '/login'
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^portal/$', views.portal, name='portal'),
    url(r'^test/$', views.test, name='test'),

]
