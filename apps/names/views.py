#!/usr/bin/python
# coding: utf-8
from __future__ import unicode_literals

import json
import datetime
import pytz
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.views.generic.detail  import DetailView
from django.views.generic.list import ListView
from categories.models import Category
from names.models import Name, Query, LetterCount


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class NamesList(ListView):
    model = Name
    context_object_name = 'names'
    template_name = 'names_list.html'
    output_all = False
    startswith = False
    days_last = 5

    def get_context_data(self, **kwargs):
        alphabet = LetterCount.objects.filter(count__gt=0).order_by('letter')

        context = super(NamesList, self).get_context_data(**kwargs)
        context['total_names'] = len(self.get_queryset())
        context['output_all'] = self.output_all
        context['query'] = self.request.GET.get('query')
        context['categories'] = Category.objects.all()
        category = self.request.GET.get('category')
        context['current_category_id'] = int(category if category else 0)
        context['alphabet'] = alphabet
        context['existed_parameters'] = self.get_existed_parameters()

        latest_letter_count = alphabet[0]
        delta = datetime.datetime.now(pytz.utc) - latest_letter_count.date_modified
        if delta.days > self.days_last:
            for letter in alphabet:
                letter.count = Name.objects.filter(visible=True, title__istartswith=letter.letter).count()
                letter.save()

        query = self.request.GET.get('query')
        female = self.request.GET.get('female')
        male = self.request.GET.get('male')
        category_id = self.request.GET.get('category')

        if query:
            # save user's query in database
            query = Query(q_text=query, q_ip=get_client_ip(self.request))
            if category_id:
                category = Category.objects.filter(id=int(category_id))[0]
                query.q_category = category
            if female:
                query.q_female = True
            if male:
                query.q_male = True
            query.save()

        return context

    def get_queryset(self):
        queryset = Name.objects.order_by('title')

        query = self.request.GET.get('query')
        female = self.request.GET.get('female')
        male = self.request.GET.get('male')
        category_id = self.request.GET.get('category')
        startswith = self.request.GET.get('startswith')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(desc__icontains=query) | Q(notes__icontains=query)
            )

        if female and not male:
            queryset = queryset.filter(gender_female=True, gender_male=False)
        elif not female and male:
            queryset = queryset.filter(gender_female=False, gender_male=True)

        if category_id:
            category = Category.objects.filter(id=int(category_id)).get()
            if category:
                queryset = queryset.filter(category=category)

        if startswith:
            queryset = queryset.filter(title__istartswith=startswith)

        if not self.request.user.is_authenticated():
            queryset = queryset.exclude(visible=False)
        return queryset

    def get_existed_parameters(self):
        result = []
        query = self.request.GET.get('query')
        female = self.request.GET.get('female')
        male = self.request.GET.get('male')
        category_id = self.request.GET.get('category')
        startswith = self.request.GET.get('startswith')
        if startswith:
            result.append('startswith={0}'.format(startswith))
        if query:
            result.append('query={0}'.format(query))
        if male:
            result.append('male=true')
        if female:
            result.append('female=true')
        if category_id:
            result.append('category={0}'.format(category_id))
        return '?{0}'.format('&'.join(result)) if result else ''


class NameView(DetailView):
    model = Name
    context_object_name = 'name'
    slug_field = 'title'
    slug_url_kwarg = 'name'
    template_name = 'names_detail.html'
