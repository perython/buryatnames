#!/usr/bin/python
# coding: utf-8
from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from categories.models import Category


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
