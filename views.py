#!/usr/bin/python
# coding: utf-8
from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from categories.models import Category
from names.models import Name


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['total_names'] = len(self.get_queryset())
        context['categories'] = Category.objects.all()
        context['current_category_id'] = int(self.request.GET.get('category') if self.request.GET.get('category') else 0)
        return context

    def get_queryset(self):
        queryset = Name.objects.all()
        if not self.request.user.is_authenticated():
            return queryset.exclude(visible=False)

        #self.cmp_names()
        #self.cptl_ttls()
        return queryset

    def cptl_ttls(self):
        names = Name.objects.all()
        for name in names:
            name.title = name.title.capitalize()
            #name.visible = True
            name.save()

    def cmp_names(self):
        f = open('/home/perython/projects/buryatnames/burnames.txt')
        fout = open('/home/perython/projects/buryatnames/out2.txt', 'w')
        san_c, tib_c, bur_c, non_c = 0, 0, 0, 0
        for line in f:
            sline = line.split('/')
            name = sline[0].strip()
            cat = sline[1].strip()
            try:
                desc = sline[2].strip()
            except:
                print sline
            try:
                notes = sline[3].strip()
            except:
                notes = ''
            q = Name.objects.filter(title__icontains=name)
            if not q:
                category_id = 2
                if 'бур' in cat:
                    category_id = 4
                    bur_c += 1
                elif 'сан' in cat:
                    category_id = 1
                    san_c += 1
                elif 'тиб' in cat:
                    category_id = 3
                    tib_c += 1
                else:
                    non_c += 1
                category = Category.objects.get(pk=category_id)

                new_name = Name(
                    title=name,
                    desc=desc,
                    notes=notes,
                    category=category,
                    visible=True
                )
                new_name.save()

        fout.write('тибетских имен = ' + str(tib_c) + '\n')
        fout.write('бурятских имен = ' + str(bur_c) + '\n')
        fout.write('санскритских имен = ' + str(san_c) + '\n')
        fout.write('без категории имен = ' + str(non_c) + '\n')

        f.close()
        fout.close()