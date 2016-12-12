# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.conf import settings as base_settings


class B3datepickerConfig(AppConfig):
    name = 'b3datepicker'


class Settings(object):
    BOOTSTRAP_DATEPICKER_VERSION = '1.6.4'
    B3DATEPICKER_JS = '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/{}/js/bootstrap-datepicker.min.js'.format(
        BOOTSTRAP_DATEPICKER_VERSION)
    B3DATEPICKER_CSS = '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/{}/css/bootstrap-datepicker3.min.css'.format(
        BOOTSTRAP_DATEPICKER_VERSION)

    def __getattribute__(self, name):
        if hasattr(base_settings, name):
            return getattr(base_settings, name)
        return object.__getattribute__(self, name)


settings = Settings()
