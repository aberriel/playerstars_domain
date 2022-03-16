from datetime import datetime
from typing import List

from marshmallow import fields, post_load
from marshmallow_enum import EnumField

from clapy_basic_classes.basic_domain.basic_value import BasicValue
from playerstars_domain.tournament.tournament_status import \
    TournamentStatus
from playerstars_domain.utils.marshmallow_helper import REQUIRED, \
    REQUIRED_DATE
import logging


class TournamentPhase(BasicValue):
    def __init__(self,
                 duels: List[str],
                 phase: TournamentStatus,
                 start_datetime: datetime):
        super(TournamentPhase, self).__init__()
        self.duels = duels
        self.phase = phase
        self.start_datetime = start_datetime
        self.logger = logging.getLogger(__name__)

    def set_logger(self, logger):
        self.logger = logger

    class Schema(BasicValue.Schema):
        duels = fields.List(
            fields.String, required=True, many=True)
        phase = EnumField(TournamentStatus, **REQUIRED)
        start_datetime = fields.AwareDateTime(**REQUIRED_DATE)

        @post_load
        def post_load(self, data, many, partial):
            return TournamentPhase(**data)
