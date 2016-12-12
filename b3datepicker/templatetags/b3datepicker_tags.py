# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe

from b3datepicker.conf import settings
from b3datepicker.widgets import get_supported_language

register = template.Library()


@register.simple_tag
def b3datepicker_css():
    css_template = u'<link rel="stylesheet" href="{}" type="text/css" charset="utf-8">'
    css = css_template.format(settings.B3DATEPICKER_CSS)
    return mark_safe(css)


@register.simple_tag(takes_context=True)
def b3datepicker_js(context):
    lang = context['LANGUAGE_CODE']
    language = get_supported_language(lang)
    js_template = u'<script src="{}" type="text/javascript" charset="utf-8"></script>'
    js = js_template.format(settings.B3DATEPICKER_JS)
    if language != 'en':
        lang_template = \
            u"//cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/{}/locales/bootstrap-datepicker.{}.min.js".format(
                settings.BOOTSTRAP_DATEPICKER_VERSION,
                language
            )
        js += js_template.format(lang_template)
    return mark_safe(js)
