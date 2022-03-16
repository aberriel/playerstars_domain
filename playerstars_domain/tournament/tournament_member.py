from clapy_basic_classes import BasicValue
from enum import Enum

from marshmallow import fields, post_load
from marshmallow_enum import EnumField

from playerstars_domain.utils.marshmallow_helper import REQUIRED


class TournamentMemberStatus(Enum):
    INVITED = 'INVITED'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    OWNER = 'OWNER'


class TournamentMember(BasicValue):
    def __init__(self,
                 member_id: str,
                 status: TournamentMemberStatus):
        super().__init__()
        self.member_id = member_id
        self.status = status

    class Schema(BasicValue.Schema):
        member_id = fields.String(**REQUIRED)
        status = EnumField(TournamentMemberStatus, **REQUIRED)

        @post_load
        def on_load(self, data, many, partial):
            return TournamentMember(**data)
