from django.conf.urls import url

from . import views
from .views import IndexView

urlpatterns = [
    # '/'
    url(r'^$', IndexView.as_view(), name='index'),

    url(r'^list/$', views.data_list, name='data_list'),
    url(r'^upload/$', views.upload2extract, name='upload2extract'),
    url(r'^delete/(?P<filename>.*)/$', views.delete, name='delete'),
    url(r'^renderer/(?P<filename>.*)/(?P<atype>.*)/$', views.renderer, name='renderer'),
    url(r'^chart/(?P<filename>.*)/(?P<atype>.*)/$', views.chart, name='chart'),
]
