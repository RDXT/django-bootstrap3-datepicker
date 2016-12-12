# -*- coding: utf-8 -*-
import re

from django.forms import DateTimeInput, DateInput, TimeInput
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

    def __init__(self, attrs=None, options=None, component=False, usel10n=None):
        self.component = component
        self.is_localized = False
        self.format = None
        self.options = options

        if self.options is None:
            self.options = {}

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
            # We set properties as underscore string
            underscore = re.sub('([A-Z]+)', r'-\1', k).lower()
            # we convert value to string (mainly for boolean values)
            attrs["data-date-%s" % underscore] = str(v)

        super(B3datepickerMixin, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if not self.component:
            attrs["data-provide"] = "datepicker"

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        rendered_widget = super(B3datepickerMixin, self).render(name, value, final_attrs)

        if self.component:
            return format_html(COMPONENT_TEMPLATE, rendered_widget, self.glyphicon)

        return rendered_widget


class DateTimeWidget(B3datepickerMixin, DateTimeInput):
    """
    DateTimeWidget is the corresponding widget for Datetime field, it renders both the date and time
    sections of the datetime picker.
    """

    format_name = 'DATETIME_INPUT_FORMATS'
    glyphicon = 'glyphicon-th'

    def __init__(self, attrs=None, options=None, usel10n=None):

        if options is None:
            options = {}

        # Set the default options to show only the datepicker object
        options['format'] = options.get('format', 'dd/mm/yyyy hh:ii')

        super(DateTimeWidget, self).__init__(attrs, options, usel10n)


class DateWidget(B3datepickerMixin, DateInput):
    """
    DateWidget is the corresponding widget for Date field, it renders only the date section of
    datetime picker.
    """

    format_name = 'DATE_INPUT_FORMATS'
    glyphicon = 'glyphicon-calendar'

    def __init__(self, attrs=None, options=None, usel10n=None):

        if options is None:
            options = {}

        # Set the default options to show only the datepicker object
        options['startView'] = options.get('startView', 2)
        options['minView'] = options.get('minView', 2)
        options['format'] = options.get('format', 'dd/mm/yyyy')

        super(DateWidget, self).__init__(attrs, options, usel10n)


class TimeWidget(B3datepickerMixin, TimeInput):
    """
    TimeWidget is the corresponding widget for Time field, it renders only the time section of
    datetime picker.
    """

    format_name = 'TIME_INPUT_FORMATS'
    glyphicon = 'glyphicon-time'

    def __init__(self, attrs=None, options=None, usel10n=None):

        if options is None:
            options = {}

        # Set the default options to show only the timepicker object
        options['startView'] = options.get('startView', 1)
        options['minView'] = options.get('minView', 0)
        options['maxView'] = options.get('maxView', 1)
        options['format'] = options.get('format', 'hh:ii')

        super(TimeWidget, self).__init__(attrs, options, usel10n)
