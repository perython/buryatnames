#!/usr/bin/python
# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Name(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    visible = models.BooleanField()

    category = models.ForeignKey('categories.Category', related_name='categories')
    title = models.CharField(max_length=300)
    desc = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    gender_male = models.BooleanField(default=True)
    gender_female = models.BooleanField(default=True)

    def __unicode__(self):
        return 'Name "{0}" ({1})'.format(self.title, self.id)

    def get_edit_url(self):
        return '/admin/names/name/{0}/'.format(self.id)


class Query(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True)

    q_text = models.CharField(max_length=255)
    q_male = models.BooleanField(default=False)
    q_female = models.BooleanField(default=False)
    q_category = models.ForeignKey('categories.Category', related_name='q_categories', null=True, blank=True)
    q_ip = models.CharField(max_length=31, null=True, blank=True)

    def __unicode__(self):
        return 'Query "{0}" ({1})'.format(self.q_text, self.id)


class LetterCount(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    letter = models.CharField(max_length=1)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return '{0}, count = {1}'.format(self.letter, self.count)
