from collections import namedtuple
from datetime import datetime
from unittest.mock import MagicMock, patch

from clapy_basic_classes.basic_domain.util import generic_serialize_roundtrip_test
from clapy_basic_classes.basic_scheduler_adapter.basic_scheduler_adapter \
    import TaskNotFoundException
from pytest import fixture

from playerstars_domain.event_reminder_assistant import (
    EventReminderAssistant,
    EraAction)

from playerstars_domain.event_reminder_assistant.event_reminder_assistant import era_factory
from playerstars_domain.utils.datetime_helper import aware_utc


@fixture
def url():
    return 'https://minhaapi.com/minha_acao'


Factory = namedtuple(
    'Factory',
    'era, mock_name, mock_event_time, mock_action, '
    'mock_persist_adapter, mock_scheduler_adapter')


@fixture
def era_factory_fixture():
    def factory(mock_name=MagicMock(),
                mock_event_time=MagicMock(),
                mock_action=MagicMock(),
                mock_persist_adapter=MagicMock(),
                mock_scheduler_adapter=MagicMock()) -> Factory:
        era = era_factory(mock_name,
                          mock_event_time,
                          mock_action,
                          mock_persist_adapter,
                          mock_scheduler_adapter)
        return Factory(era, mock_name, mock_event_time, mock_action,
                       mock_persist_adapter, mock_scheduler_adapter)

    return factory


def test_era_serialization(url):
    mock_name = 'dummy_era'
    mock_time = aware_utc(datetime(2020, 1, 1, 14, 30))
    mock_action = EraAction(url=url, method='POST', payload=dict(resposta=42))
    obj = EventReminderAssistant(mock_name, mock_time, mock_action)
    generic_serialize_roundtrip_test(EventReminderAssistant, obj)


def test_era_serialization_no_payload(url):
    mock_name = 'dummy_era'
    mock_time = aware_utc(datetime(2020, 1, 1, 14, 30))
    mock_action = EraAction(url=url, method='POST')
    obj = EventReminderAssistant(mock_name, mock_time, mock_action)
    generic_serialize_roundtrip_test(EventReminderAssistant, obj)


def test_era_factory():
    mock_name = MagicMock()
    mock_event_time = MagicMock()
    mock_action = MagicMock()
    mock_persist_adapter = MagicMock()
    mock_scheduler_adapter = MagicMock()

    result = era_factory(
        name=mock_name,
        event_time=mock_event_time,
        action=mock_action,
        persist_adapter=mock_persist_adapter,
        scheduler_adapter=mock_scheduler_adapter,
    )

    assert isinstance(result, EventReminderAssistant)
    assert result.name == mock_name
    assert result.event_time == mock_event_time
    assert result.action == mock_action
    assert result.adapter == mock_persist_adapter
    assert result.scheduler_adapter == mock_scheduler_adapter


@patch.object(EventReminderAssistant, '_set_scheduler')
def test_era_save(mock_set_scheduler, era_factory_fixture):
    fac: Factory = era_factory_fixture()
    era: EventReminderAssistant = fac.era
    era.save()
    fac.mock_persist_adapter.save.assert_called_once()
    mock_set_scheduler.assert_called_once()


@patch.object(EventReminderAssistant, '_update_if_sooner')
def test__set_scheduler(mock_update_if_sooner, era_factory_fixture):
    fac: Factory = era_factory_fixture()
    era: EventReminderAssistant = fac.era
    era._set_scheduler()
    mock_update_if_sooner.assert_called_once()


@patch.object(EventReminderAssistant, '_update_if_sooner')
def test_set_scheduler(mock_update_if_sooner, era_factory_fixture):
    fac: Factory = era_factory_fixture()
    era: EventReminderAssistant = fac.era
    era.set_scheduler()
    mock_update_if_sooner.assert_called_once()


@patch.object(EventReminderAssistant, '_update_if_sooner',
              side_effect=TaskNotFoundException('olá!'))
def test_set_scheduler_create(mock_update_if_sooner, era_factory_fixture):
    fac: Factory = era_factory_fixture()
    era: EventReminderAssistant = fac.era
    era._set_scheduler()
    mock_update_if_sooner.assert_called_once()
    fac.mock_scheduler_adapter.set.assert_called_once()


@patch.object(EventReminderAssistant, '_get_current_scheduler',
              return_value=MagicMock(execution_time=aware_utc(datetime(2020, 8, 22, 10, 0))))
@patch('playerstars_domain.event_reminder_assistant.event_reminder_assistant'
       '.aware_now', return_value=aware_utc(datetime(2020, 8, 20)))
def test_update_if_sooner_no_update(mock_aware_now,
                                    mock_get_current_scheduler,
                                    era_factory_fixture):
    mock_our_exec_time = aware_utc(datetime(2020, 8, 22, 10, 1))

    fac: Factory = era_factory_fixture(mock_event_time=mock_our_exec_time)
    era: EventReminderAssistant = fac.era

    era._update_if_sooner()

    mock_get_current_scheduler.assert_called_once()
    mock_current = mock_get_current_scheduler()
    assert mock_current.execution_time == aware_utc(datetime(2020, 8, 22, 10, 0))
    fac.mock_scheduler_adapter.update.assert_not_called()


@patch.object(EventReminderAssistant, '_get_current_scheduler',
              return_value=MagicMock(execution_time=datetime(2020, 8, 22, 10, 1)))
def test_update_if_sooner_update(mock_get_current_scheduler, era_factory_fixture):
    mock_our_exec_time = datetime(2020, 8, 22, 10, 0)
    fac: Factory = era_factory_fixture(mock_event_time=mock_our_exec_time)
    era: EventReminderAssistant = fac.era
    era._update_if_sooner()
    mock_get_current_scheduler.assert_called_once()
    fac.mock_scheduler_adapter.update.assert_called_once()


def test_delete(era_factory_fixture):
    mock_our_exec_time = datetime(2020, 8, 22, 10, 0)
    fac: Factory = era_factory_fixture(mock_event_time=mock_our_exec_time)
    era: EventReminderAssistant = fac.era
    era.delete()
    fac.mock_persist_adapter.delete.assert_called_once_with(era.entity_id)


def test_get_current_scheduler(era_factory_fixture):
    fac: Factory = era_factory_fixture()
    era: EventReminderAssistant = fac.era
    result = era._get_current_scheduler()
    fac.mock_scheduler_adapter.get_current.assert_called_with(
        fac.mock_scheduler_adapter.name)
    assert result == fac.mock_scheduler_adapter.get_current()


# def test_runner():
#     mock_name = MagicMock()
#     mock_scheduler_adapter = MagicMock()
#     mock_persist_adapter = MagicMock()
#     mock_logger = MagicMock()
#     mock_era_runner_class = MagicMock()
#     EventReminderAssistant.runner(
#         mock_name,
#         mock_scheduler_adapter,
#         mock_persist_adapter,
#         mock_era_runner_class,
#         mock_logger)
#
#     mock_era_runner_class.assert_called_with(
#         name=mock_name,
#         scheduler_adapter=mock_scheduler_adapter,
#         persist_adapter=mock_persist_adapter,
#         logger=mock_logger)
#
#     mock_era_runner_class().run.assert_called_once()
