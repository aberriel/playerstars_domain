from datetime import datetime
from unittest.mock import MagicMock

from playerstars_domain import Notification
from tests.util import generic_serialize_roundtrip_test


notification = Notification(
    entity_id='notification123',
    player_id='schrubles',
    creation_datetime=datetime(2020, 5, 31, 21, 0, 0),
    duel_id='gluglu')


def test_create_notification():
    assert notification


def test_roundtrip():
    generic_serialize_roundtrip_test(Notification, notification)


def test_notification_save():
    notification = Notification(
        player_id=MagicMock())
    notification.adapter = MagicMock()
    saved_id = notification.save_graphql()
    notification.adapter.save.assert_called_with(notification, False)
    assert saved_id == notification.adapter.save()
