#!/usr/bin/python
# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin
from names.models import Name, Query, LetterCount


class NameAdmin(admin.ModelAdmin):
    list_display = ('title', 'gender_male', 'gender_female', 'category', 'date_created')
    search_fields = ('title', 'desc', 'gender_male', 'gender_female', 'category__name')
    date_hierarchy = 'date_created'
    ordering = ('title',)


class QueryAdmin(admin.ModelAdmin):
    list_display = ('q_text', 'date_created')
    search_fields = ('q_text', 'date_created')
    date_hierarchy = 'date_created'
    ordering = ('-date_created',)


class LetterCountAdmin(admin.ModelAdmin):
    list_display = ('letter', 'count', 'date_modified')
    search_fields = ('letter', 'count')
    ordering = ('letter',)


admin.site.register(Name, NameAdmin)
admin.site.register(Query, QueryAdmin)
admin.site.register(LetterCount, LetterCountAdmin)