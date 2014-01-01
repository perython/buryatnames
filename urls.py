#!/usr/bin/python
# coding: utf-8
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import HomeView
from names.views import NamesList, NameView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^catalog/$', NamesList.as_view(paginate_by=20), name='catalog'),
    url(r'^catalog/all/$', NamesList.as_view(output_all=True), name='catalog_all'),
    url(r'^catalog/page(?P<page>\d+)/$', NamesList.as_view(paginate_by=20), name='catalog_page'),
    url(r'^name/(?P<name>[\w\W]+)$', NameView.as_view(), name='name_detail'),
)
