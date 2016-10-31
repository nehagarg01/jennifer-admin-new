from __future__ import absolute_import
import json

from django import template, VERSION
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.template import Library


register = template.Library()


@register.filter
def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return json.dumps(object)
