from clapy_basic_classes import BasicEntity
from enum import Enum

from marshmallow import fields, post_load
from marshmallow_enum import EnumField

from playerstars_domain.console import Console
from playerstars_domain.duel.duel_result import (
    ComponentResult,
    DuelComponentResult)
from playerstars_domain.game import Game
from playerstars_domain.player import CoinType
from playerstars_domain.utils.datetime_helper import aware_now
from playerstars_domain.duel.duel_judger import DuelReportState


class DefiantNotFound(BaseException):
    pass


class DuelNotDuelingException(BaseException):
    pass


class DuelStatus(Enum):
    LOBBY = 'LOBBY'
    REJECTED = 'REJECTED'
    DUELING = 'DUELING'
    CANCELED_BY_INCONSISTENT_RESULT = 'CANCELED_BY_INCONSISTENT_RESULT'
    CANCELED_BY_TIMEOUT = 'CANCELED_BY_TIMEOUT'
    UNDER_REVIEW = 'UNDER_REVIEW'
    FINISHED_ONE_SIDE = 'FINISHED_ONE_SIDE'
    FINISHED_BY_VICTORY = 'FINISHED_BY_VICTORY'
    FINISHED_BY_TIE = 'FINISHED_BY_TIE'
    FINISHED_BY_RESIGN = 'FINISHED_BY_RESIGN'
    DELETED = 'DELETED'


class DuelMemberType(Enum):
    PLAYER = 'PLAYER'
    TEAM = 'TEAM'


class DuelType(Enum):
    INDIVIDUAL = 'INDIVIDUAL'
    CHAMPIONSHIP = 'CHAMPIONSHIP'


class Duel(BasicEntity):
    def __init__(self,
                 challenger,
                 game,
                 console,
                 star_type: CoinType = CoinType.GOLDEN_STAR,
                 challenged=None,
                 challenged_accept=False,
                 bet_size=0,
                 total_reward=0,
                 creation_datetime=None,
                 time_send_invitation=None,
                 time_start=None,
                 time_finish=None,
                 time_cancel=None,
                 status=DuelStatus.LOBBY,
                 member_type=DuelMemberType.PLAYER,
                 duel_type=DuelType.INDIVIDUAL,
                 winner=None,
                 challenger_last_duel=None,
                 challenged_last_duel=None,
                 challenger_confirmation=False,
                 challenged_confirmation=False,
                 challenger_duel_result=None,
                 challenged_duel_result=None,
                 challenger_duel_info=None,
                 challenged_duel_info=None,
                 participants=2,
                 championship=None,
                 championship_level=None,
                 entity_id=None,
                 time_to_finish_duel=None,
                 time_to_accept_invitation=None):
        super(Duel, self).__init__(entity_id=entity_id)
        self.challenger = challenger
        self.challenged = challenged
        self.challenged_accept = challenged_accept
        self.championship = championship
        self.championship_level = championship_level
        self.game = game
        self.console = console
        self.star_type = star_type
        self.bet_size = bet_size
        self.total_reward = total_reward or bet_size * 2
        self.creation_datetime = creation_datetime or aware_now()
        self.time_send_invitation = time_send_invitation
        self.time_start = time_start
        self.time_finish = time_finish
        self.time_cancel = time_cancel
        self.status: DuelStatus = status
        self.member_type: DuelMemberType = member_type
        self.duel_type: DuelType = duel_type
        self.winner = winner
        self.challenger_last_duel = challenger_last_duel
        self.challenged_last_duel = challenged_last_duel
        self.challenger_confirmation = challenger_confirmation
        self.challenged_confirmation = challenged_confirmation
        self.challenger_duel_result = challenger_duel_result
        self.challenged_duel_result = challenged_duel_result
        self.challenger_duel_info = challenger_duel_info
        self.challenged_duel_info = challenged_duel_info
        self.participants = participants
        self.time_to_finish_duel = time_to_finish_duel
        self.time_to_accept_invitation = time_to_accept_invitation

    def save_graphql(self, exec_update=False):
        my_id = self.adapter.save(self, exec_update)
        return my_id

    def challenger_confirmed(self):
        self.challenger_confirmation = True

    def challenged_confirmed(self):
        self.challenged_confirmation = True

    def increase_bet_size(self, amount):
        self.bet_size = self.bet_size + amount

    def decrease_bet_size(self, amount):
        if amount > self.bet_size:
            raise ValueError("Não é possivel ter apostas negativas")
        self.bet_size = self.bet_size - amount

    def submit_result(self,
                      defiant_id: str,
                      result: ComponentResult,
                      image_path=None):
        if self.status != DuelStatus.DUELING:
            raise DuelNotDuelingException('Duel not in progress status.')

        result = DuelComponentResult(result=result, result_image=image_path)
        if self.challenger == defiant_id:
            self.challenger_duel_result = result
        elif self.challenged == defiant_id:
            self.challenged_duel_result = result
        else:
            raise DefiantNotFound(f'Defiant {defiant_id} not found')

    class Schema(BasicEntity.Schema):
        OPTIONAL_DATE = dict(format='iso', required=False, allow_none=True)
        REQUIRED_DATE = dict(format='iso', required=True, allow_none=False,
                             default=aware_now)

        challenger = fields.String(required=True, allow_none=False)
        challenged = fields.String(required=False, allow_none=True)
        challenged_accept = fields.Boolean(default=False, missing=False)
        championship = fields.String(required=False, allow_none=True)
        championship_level = fields.Integer(required=False, allow_none=True)
        game = fields.Nested(Game.Schema, required=True)
        console = fields.Nested(Console.Schema, required=True)
        star_type = EnumField(
            CoinType,
            required=True,
            allow_none=False,
            default=CoinType.GOLDEN_STAR)
        bet_size = fields.Integer(required=True, default=0)
        participants = fields.Integer(required=True, default=2)
        total_reward = fields.Integer(required=True, default=0)
        creation_datetime = fields.AwareDateTime(**REQUIRED_DATE)
        time_send_invitation = fields.AwareDateTime(**OPTIONAL_DATE)
        time_start = fields.AwareDateTime(**OPTIONAL_DATE)
        time_finish = fields.AwareDateTime(**OPTIONAL_DATE)
        time_cancel = fields.AwareDateTime(**OPTIONAL_DATE)
        winner = fields.String(required=False, default=None, allow_none=True)
        challenger_last_duel = fields.String(required=False, allow_none=True)
        challenged_last_duel = fields.String(required=False, allow_none=True)
        challenger_confirmation = fields.Boolean(default=False, missing=False)
        challenged_confirmation = fields.Boolean(default=False, missing=False)
        challenger_duel_result = fields.Nested(
            DuelComponentResult.Schema, required=False, allow_none=True)
        challenged_duel_result = fields.Nested(
            DuelComponentResult.Schema, required=False, allow_none=True)
        challenger_duel_info = EnumField(
            DuelReportState, required=False, allow_none=True, default=None)
        challenged_duel_info = EnumField(
            DuelReportState, required=False, allow_none=True, default=None)
        status = EnumField(
            DuelStatus,
            required=True,
            allow_none=False,
            default=DuelStatus.LOBBY)
        member_type = EnumField(
            DuelMemberType,
            required=True,
            allow_none=False,
            default=DuelMemberType.PLAYER)
        duel_type = EnumField(
            DuelType,
            required=True,
            allow_none=False,
            default=DuelType.INDIVIDUAL)
        time_to_finish_duel = fields.Integer(required=True, allow_none=False)
        time_to_accept_invitation = fields.Integer(required=True,
                                                   allow_none=False)

        @post_load
        def post_load(self, data, many, partial):
            return Duel(**data)
