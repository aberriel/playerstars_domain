from clapy_basic_classes import BasicEntity
from enum import Enum
from marshmallow import fields, post_load
from marshmallow_enum import EnumField
from playerstars_domain.utils.datetime_helper import aware_now


class NotificationStatus(Enum):
    CREATED = 'CREATED'
    SENT = 'SENT'
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    DELETED = 'DELETED'


class NotificationType(Enum):
    INFORMATIVE = 'INFORMATIVE'
    CHAMPIONSHIP_INVITE_PLAYER = 'CHAMPIONSHIP_INVITE_PLAYER'
    CHAMPIONSHIP_INVITE_TEAM = 'CHAMPIONSHIP_INVITE_TEAM'
    CHAMPIONSHIP_START = 'CHAMPIONSHIP_START'
    CHAMPIONSHIP_FINISH = 'CHAMPIONSHIP_FINISH'
    CHAMPIONSHIP_CANCEL = 'CHAMPIONSHIP_CANCEL'
    TEAM_INVITE = 'TEAM_INVITE'
    DUEL_INVITE = 'DUEL_INVITE'
    DUEL_INVITE_ACCEPTED = 'DUEL_INVITE_ACCEPTED'
    DUEL_INVITE_REJECTED = 'DUEL_INVITE_REJECTED'
    DUEL_ONGOING = 'DUEL_ONGOING'
    DUEL_CANCEL_BY_TIMEOUT = 'DUEL_CANCEL_BY_TIMEOUT'
    DUEL_CANCEL_BY_CREATOR = 'DUEL_CANCEL_BY_CREATOR'
    DUEL_FINISHED_CONFLICT = 'DUEL_FINISHED_CONFLICT'
    DUEL_FINISHED_WINNER = 'DUEL_FINISHED_WINNER'
    DUEL_FINISHED_LOSER = 'DUEL_FINISHED_LOSER'
    DUEL_TIED = 'DUEL_TIED'


class Notification(BasicEntity):
    def __init__(self,
                 player_id: str,
                 status: NotificationStatus = NotificationStatus.CREATED,
                 creation_datetime=None,
                 notification_type: NotificationType =
                 NotificationType.INFORMATIVE,
                 entity_id: str = None,
                 duel_id: str = None,
                 team_id: str = None,
                 championship_id: str = None,
                 notification_image: str = None,
                 notification_complement: str = None,
                 additional_data: str = None):
        super(Notification, self).__init__(entity_id=entity_id)
        self.player_id = player_id
        self.duel_id = duel_id
        self.status = status
        self.team_id = team_id
        self.championship_id = championship_id
        self.creation_datetime = creation_datetime or aware_now()
        self.notification_type = notification_type
        self.notification_image = notification_image
        self.notification_complement = notification_complement
        self.additional_data = additional_data

    def save_graphql(self, exec_update=False):
        my_id = self.adapter.save(self, exec_update)
        return my_id

    class Schema(BasicEntity.Schema):
        player_id = fields.String(required=True)
        duel_id = fields.String(default=None, missing=None, allow_none=True)
        team_id = fields.String(default=None, missing=None, allow_none=True)
        championship_id = fields.String(
            default=None, missing=None, allow_none=True)
        status = EnumField(NotificationStatus, required=True)
        creation_datetime = fields.DateTime(
            format='iso', required=True, allow_none=False)
        notification_type = EnumField(
            NotificationType, required=True,
            default=NotificationType.INFORMATIVE)
        notification_image = fields.String(
            default=None, missing=None, allow_nome=True)
        notification_complement = fields.String(
            default=None, missing=None, allow_none=True)
        additional_data = fields.String(
            default=None, missing=None, allow_none=None)

        @post_load
        def post_load(self, data, many, partial):
            return Notification(**data)
