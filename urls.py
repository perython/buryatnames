#!/usr/bin/python
# coding: utf-8
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import HomeView
from names.views import NamesList, NameView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view()),
    url(r'^catalog/$', NamesList.as_view(paginate_by=20)),
    url(r'^catalog/all/$', NamesList.as_view(output_all=True)),
    url(r'^catalog/page(?P<page>\d+)/$', NamesList.as_view(paginate_by=20)),
    url(r'^name/(?P<name>[\w\W]+)$', NameView.as_view()),
)
