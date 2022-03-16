from clapy_basic_classes import BasicEntity
from datetime import datetime
from enum import Enum
from marshmallow import fields, post_load
from marshmallow_enum import EnumField
from playerstars_domain.player import Player
from playerstars_domain.team.team_member import (
    MemberStatus,
    MemberType,
    TeamMember)
from playerstars_domain.utils.datetime_helper import aware_now
from typing import List


class MemberNotFoundException(BaseException):
    pass


class TeamStatus(Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class Team(BasicEntity):
    def __init__(self,
                 name: str,
                 captain: TeamMember,
                 victories=0,
                 logo_path: str = None,
                 console_id: str = None,
                 game_id: str = None,
                 members: list = None,
                 entity_id: str = None,
                 description: str = None,
                 creation_datetime: datetime = None,
                 status: TeamStatus = TeamStatus.ACTIVE,
                 elo_rating: float = 1500):
        super(Team, self).__init__(entity_id=entity_id)
        self.name = name
        self.captain = captain
        self.logo_path = logo_path
        self.console_id = console_id
        self.members: List[TeamMember] = members if members else []
        self.description = description
        self.creation_datetime = creation_datetime or aware_now()
        self.game_id = game_id
        self.victories = victories
        self.status = status
        self.elo_rating = elo_rating

        if not self._is_captain_member():
            self.members.append(captain)

    def _is_captain_member(self):
        return self.captain.player_id in [x.player_id for x in self.members]

    @staticmethod
    def _verify_is_member_invited(mtype, status):
        if mtype == MemberType.MEMBER and status != MemberStatus.INVITED:
            raise Exception('Members can only be added as invited')

    @staticmethod
    def _verify_captain_add_as_member(mtype, status):
        if mtype == MemberType.CAPTAIN and status != MemberStatus.ACCEPTED:
            raise Exception('The captain can only be added as member')

    def add_member(self, player: Player,
                   member_type: MemberType = MemberType.MEMBER,
                   initial_status: MemberStatus = MemberStatus.INVITED):

        self._verify_is_member_invited(member_type, initial_status)
        self._verify_captain_add_as_member(member_type, initial_status)

        try:
            self.find_member_by_id(player.entity_id)
        except MemberNotFoundException:
            new_member = TeamMember(player_id=player.entity_id,
                                    association_date=aware_now(),
                                    member_type=member_type,
                                    status=initial_status)
            self.members.append(new_member)
            return True

        return False

    @staticmethod
    def _verify_not_invite_captain(member):
        if member.member_type == MemberType.CAPTAIN:
            raise Exception("Captain can't accept invitation")

    @staticmethod
    def _verify_not_already_rejected(member, status):
        if all([member.status == MemberStatus.REJECTED,
                status == MemberStatus.ACCEPTED]):
            raise Exception('The member cannot accept the invite '
                            'because he rejected the invitation')

    def _validate_invite(self, member, status):
        if status == MemberStatus.ACCEPTED:
            self._verify_is_team_full()
        Team._verify_not_invite_captain(member)
        Team._verify_not_already_rejected(member, status)

    def _is_team_full(self):
        return len(self.get_active_members()) >= 5

    def _verify_is_team_full(self):
        if self._is_team_full():
            raise Exception('The team {0} is full'.format(self.name))

    def member_invite_response(self, player_id, accept=True):
        try:
            member_found = self.find_member_by_id(player_id)
        except MemberNotFoundException:
            raise Exception("The player isn't member of this team")

        status = MemberStatus.ACCEPTED if accept else MemberStatus.REJECTED

        self._validate_invite(member_found, status)

        member_found.change_status(status)
        member_found.last_status_change_datetime = aware_now()

    def _is_captain(self, player_id):
        return self.captain.player_id == player_id

    def find_member_by_id(self, member_id: str):
        try:
            member = [x for x in self.members if x.player_id == member_id][0]
        except IndexError:
            raise MemberNotFoundException()

        member.member_type = MemberType.CAPTAIN \
            if self._is_captain(member.player_id) else MemberType.MEMBER

        return member

    def remove_member(self, member_id):
        if self.captain.player_id == member_id:
            raise Exception("You can't remove captain")

        try:
            self.find_member_by_id(member_id)
        except MemberNotFoundException:
            return False

        new_member_list = [x for x in self.members
                           if x.player_id != member_id]
        self.members = new_member_list
        return True

    def get_active_members(self):
        return [x for x in self.members if x.status == MemberStatus.ACCEPTED]

    def leave_team(self, player_id):
        try:
            member_found = self.find_member_by_id(player_id)
        except MemberNotFoundException:
            raise Exception("The player isn't member of this team")

        if member_found.member_type == MemberType.CAPTAIN:
            raise Exception("Captain can't be removed")
        if any([member_found.status == MemberStatus.INVITED,
                member_found.status == MemberStatus.REJECTED]):
            raise Exception('The member cannot leave '
                            'because your status is {0}'
                            .format(member_found.status.value))

        self.remove_member(member_found.player_id)

    def add_game_point(self):
        self.victories += 1

    def check_if_member(self, player_id):
        return True if player_id in [x.player_id for x in self.members] \
            else False

    class Schema(BasicEntity.Schema):
        name = fields.String(required=True, allow_none=False)
        logo_path = fields.String(required=False, allow_none=True)
        captain = fields.Nested(
            TeamMember.Schema, required=True, allow_none=False)
        console_id = fields.String(default="", missing="")
        game_id = fields.String(default="", missing="")
        members = fields.Nested(
            TeamMember.Schema, many=True, default=[],
            missing=[])
        description = fields.String(required=False, allow_none=True)
        victories = fields.Integer(
            required=False, allow_none=True, default=0)
        creation_datetime = fields.DateTime(
            format='iso', required=False, allow_none=True)
        status = EnumField(TeamStatus, required=True)
        elo_rating = fields.Float(required=False,
                                  allow_none=False,
                                  default=1500,
                                  missing=1500)

        @post_load
        def post_load(self, data, many, partial):
            return Team(**data)
