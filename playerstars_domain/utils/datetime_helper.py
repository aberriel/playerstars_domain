from datetime import datetime

import pytz


def aware_now():
    return datetime.utcnow().replace(tzinfo=pytz.utc)


def aware_utc(value: datetime):
    return value.replace(tzinfo=pytz.utc)
