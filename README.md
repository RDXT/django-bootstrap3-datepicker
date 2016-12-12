# django-bootstrap3-datepicker

A lot of code borrowed/inspired by django-datetime-widget

Add 'b3datepicker' to installed apps.

# Static
```
{% load b3datepicker_tags %}
{% b3datepicker_css %}
{% b3datepicker_js %}
{{form.media}}
```

By default loads the following version css and js:
```
BOOTSTRAP_DATEPICKER_VERSION = '1.6.4'
B3DATEPICKER_JS = '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.6.4/js/bootstrap-datepicker.min.js'
B3DATEPICKER_CSS = '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.6.4/css/bootstrap-datepicker3.min.css'
```
If you just want to use a more recent version available on cdnjs just add BOOTSTRAP_DATEPICKER_VERSION = '1.whatever'

# Available options

Pretty much all the options except the function based ones from:

https://bootstrap-datepicker.readthedocs.io/en/stable/options.html

You can add options to the widget via:
```
widget=DateWidget(
            usel10n=True,
            options={
                'endDate': '0d',
            }
        )
```

If you dont want to show a calendar icon from the component markup:

https://bootstrap-datepicker.readthedocs.io/en/stable/markup.html
```
widget=DateWidget(
            usel10n=True,
            options={
                'endDate': '0d',
            },
            component_view=False
        )
```