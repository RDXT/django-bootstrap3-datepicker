# -*- coding: utf-8 -*-
import re

from django.forms import DateInput
from django.utils.formats import get_format
from django.utils.html import format_html
from django.utils.translation import get_language

supported_locales = [
    'ar', 'az', 'bg', 'bs', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en-AU', 'en-GB', 'eo', 'es', 'et', 'eu', 'fa', 'fi',
    'fo', 'fr-CH', 'fr', 'gl', 'he', 'hr', 'hu', 'hy', 'id', 'is', 'it-CH', 'it', 'ja', 'ka', 'kh', 'kk', 'ko', 'kr',
    'lt', 'lv', 'me', 'mk', 'mn', 'ms', 'nb', 'nl-BE', 'nl', 'no', 'pl', 'pt-BR', 'pt', 'ro', 'rs-latin', 'rs', 'ru',
    'sk', 'sl', 'sq', 'sr-latin', 'sr', 'sv', 'sw', 'th', 'tr', 'uk', 'vi', 'zh-CN', 'zh-TW'
]


def get_supported_language(language_country_code):
    if not language_country_code:
        return 'en'

    if language_country_code in supported_locales:
        return language_country_code

    language = language_country_code.split('-')[0]
    if language in supported_locales:
        return language

    return 'en'


dateConversiontoPython = {
    'P': '%p',
    'ss': '%S',
    'ii': '%M',
    'hh': '%H',
    'HH': '%I',
    'dd': '%d',
    'mm': '%m',
    'yy': '%y',
    'yyyy': '%Y',
}

toPython_re = re.compile(r'\b(' + '|'.join(dateConversiontoPython.keys()) + r')\b')

dateConversiontoJavascript = {
    '%M': 'ii',
    '%m': 'mm',
    '%I': 'HH',
    '%H': 'hh',
    '%d': 'dd',
    '%Y': 'yyyy',
    '%y': 'yy',
    '%p': 'P',
    '%S': 'ss'
}

toJavascript_re = re.compile(r'(?<!\w)(' + '|'.join(dateConversiontoJavascript.keys()) + r')\b')

COMPONENT_TEMPLATE = """
       <div class="input-group date" data-provide="datepicker">
            {}
            <div class="input-group-addon">
                <span class="glyphicon {}"></span>
            </div>
        </div>
       """


class B3datepickerMixin(object):
    format_name = None
    glyphicon = None

    def __init__(self, attrs=None, options=None, component_view=False, usel10n=None):
        self.component_view = component_view
        self.is_localized = False
        self.format = None
        self.options = options

        if self.options is None:
            self.options = {}

        # set some defaults
        self.options.setdefault('autoclose', True)
        self.options.setdefault('assumeNearbyYear', True)
        self.options.setdefault('todayHighlight', True)
        self.options.setdefault('weekStart', 1)
        self.options.setdefault('calendarWeeks', True)
        self.options.setdefault('clearBtn', False)

        if usel10n is True:
            self.is_localized = True

            self.format = get_format(self.format_name)[0]

            self.options['format'] = toJavascript_re.sub(
                lambda x: dateConversiontoJavascript[x.group()],
                self.format
            )

            self.options['language'] = get_supported_language(get_language())

        else:
            format = self.options['format']
            self.format = toPython_re.sub(
                lambda x: dateConversiontoPython[x.group()],
                format
            )

        if attrs is None:
            attrs = {}
        for k, v in self.options.items():
            if isinstance(v, bool):
                v = {True: 'true', False: 'false'}[v]
            # set properties
            pattern = re.sub('([A-Z]+)', r'-\1', k).lower()
            # we convert value to string (mainly for boolean values)
            attrs["data-date-%s" % pattern] = str(v)

        super(B3datepickerMixin, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if not self.component_view:
            attrs["data-provide"] = "datepicker"

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        rendered_widget = super(B3datepickerMixin, self).render(name, value, final_attrs)

        print self.component_view
        if self.component_view:
            return format_html(COMPONENT_TEMPLATE, rendered_widget, self.glyphicon)

        return rendered_widget


class DateWidget(B3datepickerMixin, DateInput):
    format_name = 'DATE_INPUT_FORMATS'
    glyphicon = 'glyphicon-calendar'

    def __init__(self, attrs=None, options=None, component_view=False, usel10n=None):

        if options is None:
            options = {}

        # Set the default options to show only the datepicker object
        options['format'] = options.get('format', 'dd/mm/yyyy')

        super(DateWidget, self).__init__(attrs, options, component_view, usel10n)
