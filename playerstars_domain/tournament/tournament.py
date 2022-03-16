from datetime import datetime, timedelta
from typing import List
from math import log, ceil
from abc import abstractmethod

from marshmallow import fields, post_load
from marshmallow_enum import EnumField

from clapy_basic_classes.basic_domain.basic_entity import BasicEntity
from playerstars_domain.console import Console
from playerstars_domain.game import Game
from playerstars_domain.tournament.tournament_member import \
    TournamentMember, TournamentMemberStatus
from playerstars_domain.utils.marshmallow_helper import REQUIRED, \
    REQUIRED_DATE, required_date_default_now
from playerstars_domain.tournament.tournament_status import \
    TournamentStatus
from playerstars_domain.tournament.phase import TournamentPhase
import logging


class Tournament(BasicEntity):
    def __init__(self,
                 game: Game,
                 console: Console,
                 award_first_place_perc: int,
                 award_second_place_perc: int,
                 award_third_place_perc: int,
                 price_to_enter: int,
                 member_amount: int,
                 level_duration: int,
                 levels_per_day: int,
                 start_datetime: datetime,
                 members: List[TournamentMember],
                 status: TournamentStatus,
                 creation_datetime: datetime,
                 phases: List[TournamentPhase] = None,
                 entity_id=None):
        super(Tournament, self).__init__(entity_id=entity_id)
        self.game = game
        self.console = console
        self.award_first_place_perc = award_first_place_perc
        self.award_second_place_perc = award_second_place_perc
        self.award_third_place_perc = award_third_place_perc
        self.price_to_enter = price_to_enter
        self.member_amount = member_amount
        self.level_duration = level_duration
        self.levels_per_day = levels_per_day
        self.start_datetime = start_datetime
        self.members = members
        self.phases = phases
        self.status = status
        self.creation_datetime = creation_datetime
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def is_member(self, player_id):
        self.logger.info('TOURNAMENT')
        pass

    @property
    def star_amount(self):
        return self.price_to_enter * self.member_amount

    @property
    def phases_amount(self):
        return log(self.member_amount)/log(2)

    @property
    def finish_datetime(self):
        return self.start_datetime + timedelta(days=ceil(self.phases_amount))

    @property
    def finish_date(self):
        return datetime.strftime(self.finish_datetime, "%d/%m/%Y")

    @property
    def finish_time(self):
        return datetime.strftime(self.finish_datetime, "%H:%M:%S")

    @property
    def confirmed_members(self):
        return len([x for x in self.members if x.status in
                    [TournamentMemberStatus.ACCEPTED,
                     TournamentMemberStatus.OWNER]])

    @property
    def first_place_prize(self):
        return self.star_amount * self.award_first_place_perc/100

    @property
    def second_place_prize(self):
        return self.star_amount * self.award_second_place_perc/100

    @property
    def third_place_prize(self):
        return self.star_amount * self.award_third_place_perc/100

    @property
    def creator_id(self):
        return [x.member_id for x in self.members
                if x.status == TournamentMemberStatus.OWNER][0]

    class Schema(BasicEntity.Schema):
        game = fields.Nested(Game.Schema, **REQUIRED)
        console = fields.Nested(Console.Schema, **REQUIRED)

        award_first_place_perc = fields.Int(**REQUIRED)
        award_second_place_perc = fields.Int(**REQUIRED)
        award_third_place_perc = fields.Int(**REQUIRED)
        price_to_enter = fields.Int(**REQUIRED)
        member_amount = fields.Int(**REQUIRED)
        level_duration = fields.Int(**REQUIRED)
        levels_per_day = fields.Int(**REQUIRED)
        start_datetime = fields.AwareDateTime(**REQUIRED_DATE)

        members = fields.Nested(TournamentMember.Schema,
                                required=True,
                                many=True)
        phases = fields.Nested(TournamentPhase.Schema,
                               required=False,
                               many=True,
                               allow_none=True)
        status = EnumField(TournamentStatus, **REQUIRED)
        creation_datetime = fields.DateTime(**required_date_default_now())

        @post_load
        def post_load(self, data, many, partial):
            return Tournament(**data)
