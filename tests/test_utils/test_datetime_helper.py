from playerstars_domain.utils.datetime_helper import aware_now, aware_utc
from unittest.mock import patch, MagicMock


@patch('playerstars_domain.utils.datetime_helper.datetime')
@patch('playerstars_domain.utils.datetime_helper.pytz')
def test_aware_now(mock_pytz, mock_datetime):
    dt = aware_now()
    mock_datetime.utcnow.assert_called_once()
    mock_utcnow = mock_datetime.utcnow.return_value
    mock_utcnow.replace.assert_called_with(tzinfo=mock_pytz.utc)
    assert dt == mock_utcnow.replace.return_value


@patch('playerstars_domain.utils.datetime_helper.pytz')
def test_aware_utc(mock_pytz):
    mock_date = MagicMock()
    result = aware_utc(mock_date)
    mock_date.replace.assert_called_with(tzinfo=mock_pytz.utc)
    assert result == mock_date.replace.return_value
