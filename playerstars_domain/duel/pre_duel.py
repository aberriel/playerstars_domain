from clapy_basic_classes import BasicEntity
from enum import Enum
from marshmallow import fields, post_load
from marshmallow_enum import EnumField
from playerstars_domain.duel import DuelMemberType
from playerstars_domain.player import CoinType


class Status(Enum):
    AWAITING = 'AWAITING'
    CONFIRM = 'CONFIRM'
    CONFIRMED_1 = 'CONFIRMED_1'
    CONFIRMED_2 = 'CONFIRMED_2'
    ACCEPTED_1 = 'ACCEPTED_1'
    ACCEPTED_2 = 'ACCEPTED_2'
    REFUSED = 'REFUSED'
    TIMED_OUT = 'TIMED_OUT'


class PreDuel(BasicEntity):
    def __init__(self,
                 status: Status,
                 game_entity_id: str,
                 console_entity_id: str,
                 star_type,
                 duel_type,
                 star_amount,
                 challenger,
                 challenged,
                 ack,
                 duel_id: str = None,
                 entity_id: str = None):
        super(PreDuel, self).__init__(entity_id=entity_id)
        self.status = status
        self.game_entity_id = game_entity_id
        self.console_entity_id = console_entity_id
        self.star_type = star_type
        self.duel_type = duel_type
        self.star_amount = star_amount
        self.challenger = challenger
        self.challenged = challenged
        self.ack = ack
        self.duel_id = duel_id

    class Schema(BasicEntity.Schema):
        status = EnumField(Status, required=True, allow_none=False)
        star_type = EnumField(CoinType, required=True, allow_none=False)
        duel_type = EnumField(DuelMemberType, required=True, allow_none=False)

        game_entity_id = fields.String(required=False, allow_none=True)
        console_entity_id = fields.String(required=False, allow_none=True)
        challenger = fields.String(required=False, allow_none=True)
        challenged = fields.String(required=False, allow_none=True, missing=None, default=None)
        ack = fields.Boolean(required=False, allow_none=True,
                             default=False, missing=False)
        star_amount = fields.Integer(required=False, allow_none=True)
        duel_id = fields.String(required=False, allow_none=True)

        @post_load
        def on_load(self, data, many, partial):
            return PreDuel(**data)
