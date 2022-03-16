from unittest.mock import MagicMock

from playerstars_domain.utils.datetime_helper import aware_now
from playerstars_domain.utils.marshmallow_helper import required_default, \
    required_date_default_now


def test_required_default():
    mock_default = MagicMock()
    result = required_default(mock_default)
    assert result == dict(required=True, allow_none=False, default=mock_default)


def test_required_date_default_now():
    result = required_date_default_now()
    assert result == dict(format='iso',
                          required=True,
                          allow_none=False,
                          default=aware_now)
