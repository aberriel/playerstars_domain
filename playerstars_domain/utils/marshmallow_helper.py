from playerstars_domain.utils.datetime_helper import aware_now

REQUIRED = dict(required=True, allow_none=False)
OPTIONAL_DATE = dict(format='iso', required=False, allow_none=True)
REQUIRED_DATE = dict(format='iso', required=True, allow_none=False)


def required_default(default_value):
    required = REQUIRED.copy()
    required.update(dict(default=default_value))
    return required


def required_date_default_now():
    required = REQUIRED_DATE
    required.update(dict(default=aware_now))
    return required
