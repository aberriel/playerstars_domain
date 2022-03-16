from datetime import datetime
from typing import Optional

from clapy_basic_classes import BasicEntity, BasicValue
from clapy_basic_classes.basic_domain.task_scheduler_port import \
    TaskSchedulerPort
from clapy_basic_classes.basic_persist_adapter import BasicPersistAdapter
from clapy_basic_classes.basic_scheduler_adapter import \
    BasicTaskSchedulerAdapter
from clapy_basic_classes.basic_scheduler_adapter.basic_scheduler_adapter \
    import TaskNotFoundException
from marshmallow import fields, post_load
from playerstars_domain.utils.datetime_helper import aware_utc, aware_now
from playerstars_domain.utils.marshmallow_helper import REQUIRED


class EraAction(BasicValue):
    def __init__(self,
                 url: str,
                 method: str,
                 payload: Optional[dict] = None):
        self.url = url
        self.method = method
        self.payload = payload

    class Schema(BasicValue.Schema):
        url = fields.Url(**REQUIRED)
        method = fields.Str(**REQUIRED)
        payload = fields.Dict(required=False, allow_none=True)

        @post_load
        def on_load(self, data, many, partial):
            return EraAction(**data)


def era_factory(name: str,
                event_time: datetime,
                action: EraAction,
                persist_adapter: BasicPersistAdapter,
                scheduler_adapter: BasicTaskSchedulerAdapter):
    era = EventReminderAssistant(name=name,
                                 event_time=event_time,
                                 action=action)
    era.set_adapter(persist_adapter)
    era.set_scheduler_adapter(scheduler_adapter)
    return era


class EventReminderAssistant(BasicEntity, TaskSchedulerPort):
    def __init__(self,
                 name: str,
                 event_time: datetime,
                 action: EraAction,
                 entity_id: Optional[str] = None):
        """
        ERA - EventReminderAssistant - realiza uma operação pré-determinada
              num momento definido (scheduled task)
        :param name: Nome amigável para ajudar à identificar este ERA.
        :param event_time: momento (datetime) que o EraActin deve ser executado
        :param action: EraAction que será executado
        :param entity_id: Identificador deste ERA
        """
        super().__init__(entity_id=entity_id)
        self.name = name
        self.event_time = event_time
        self.action = action

    class Schema(BasicEntity.Schema):
        name = fields.Str(**REQUIRED)
        event_time = fields.AwareDateTime(**REQUIRED)
        action = fields.Nested(EraAction.Schema, **REQUIRED)

        @post_load
        def on_load(self, data, many, partial):
            return EventReminderAssistant(**data)

    def save(self):
        super().save()
        self._set_scheduler()

    def set_scheduler(self):
        self._set_scheduler()

    def _set_scheduler(self):
        try:
            self._update_if_sooner()
        except TaskNotFoundException:
            self.scheduler_adapter.set(self.entity_id, self.event_time)

    @staticmethod
    def _is_sooner(current, event_time):
        return event_time < current or aware_utc(current) <= aware_now()

    def _update_if_sooner(self):
        current = self._get_current_scheduler().execution_time

        if self._is_sooner(current, self.event_time):
            self.scheduler_adapter.update(self.entity_id, self.event_time)

    def _get_current_scheduler(self):
        current_scheduler: BasicTaskSchedulerAdapter = \
            self.scheduler_adapter.get_current(self.scheduler_adapter.name)
        return current_scheduler

    def delete(self):
        self.adapter.delete(self.entity_id)

    # @staticmethod
    # def runner(name: str,
    #            scheduler_adapter: BasicTaskSchedulerAdapter,
    #            persist_adapter: BasicPersistAdapter,
    #            era_runner_class,
    #            logger=None):
    #     era_runner = era_runner_class(name=name,
    #                                   scheduler_adapter=scheduler_adapter,
    #                                   persist_adapter=persist_adapter,
    #                                   logger=logger)
    #     era_runner.run()
