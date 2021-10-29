from django.template import Library

from misc.utils import words
from misc.utils.constants import SHORT_DATE_FORMAT
import six

register = Library()


@register.filter(name='remove')
def remove(value, text_to_replace):
    return str(value).replace('/' + text_to_replace, '')


@register.filter(name='show_date')
def show_date(value):
    if value == '' or value is None:
        return '<span class="text-danger"><b>%s</b></span>' % words.NO_RECORDS.capitalize()
    return '<i class="fa fa-calendar-alt mr-1"></i> %s' % format(value, SHORT_DATE_FORMAT)


@register.filter(name='range_paginator')
def range_paginator(page, paginator):
    if paginator.num_pages < 11:
        begin = 1
        end = paginator.num_pages + 1
    else:
        if page.number - 5 < 1:
            begin = 1
            end = 11
        else:
            if page.number + 5 > paginator.num_pages:
                begin = page.number - (10 - (paginator.num_pages - page.number + 1))
                end = paginator.num_pages + 1
            else:
                begin = page.number - 4
                end = page.number + 6
    return six.moves.range(begin, end)


@register.filter(name='show_price')
def show_price(value):
    if not value:
        return '0.00€'
    else:
        return str('{0:.2f}€'.format(value))
