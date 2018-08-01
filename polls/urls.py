from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(),
        name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    path('function', views.function),
    path('class', views.ClassView.as_view()),
    url(r'^new_contact/$', views.new_contact, name='new_contact'),
]
