from clapy_basic_classes import BasicValue
from marshmallow import fields, post_load
from marshmallow_enum import EnumField
from playerstars_domain.utils.datetime_helper import aware_now

import enum


class MemberType(enum.Enum):
    CAPTAIN = 'CAPTAIN'
    MEMBER = 'MEMBER'


class MemberStatus(enum.Enum):
    INVITED = 'INVITED'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    GONE_OUT = 'GONE_OUT'


class TeamMember(BasicValue):
    def __init__(self, player_id: str,
                 status: MemberStatus = MemberStatus.INVITED,
                 association_date=None,
                 bet_amount: int = None,
                 member_type=None,
                 last_status_change_datetime=None):
        super(TeamMember, self).__init__()
        self.player_id = player_id
        self.association_date = association_date or aware_now()
        self.last_status_change_datetime = \
            last_status_change_datetime or aware_now()
        self.bet_amount: int = bet_amount if bet_amount else 0
        self.member_type = member_type or MemberType.MEMBER
        self.status = status

    def change_status(self, new_status: MemberStatus):
        if self.status == MemberStatus.GONE_OUT:
            raise Exception('The member has already left the team')
        if self.status == MemberStatus.REJECTED:
            raise Exception('The member has already rejected the invitation')
        if self.member_type == MemberType.CAPTAIN \
            and (new_status == MemberStatus.GONE_OUT
                 or new_status == MemberStatus.REJECTED):
            raise Exception('Captain cannot leave the team')

        self.status = new_status
        self.last_status_change_datetime = aware_now()

    class Schema(BasicValue.Schema):
        player_id = fields.String(required=True)
        association_date = fields.DateTime(
            required=True, allow_none=False, format='iso')
        last_status_change_datetime = fields.DateTime(
            required=False, allow_none=True, format='iso')
        bet_amount = fields.Integer(default=0, missing=0)
        member_type = EnumField(
            MemberType, required=True, allow_none=False,
            default=MemberType.MEMBER)
        status = EnumField(
            MemberStatus, required=True, allow_none=False,
            default=MemberStatus.INVITED)

        @post_load
        def post_load(self, data, many, partial):
            return TeamMember(**data)
