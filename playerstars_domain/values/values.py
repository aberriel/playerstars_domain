from clapy_basic_classes import BasicEntity
from marshmallow import fields, post_load
from playerstars_domain.values.validator_maps import ValidatorMaps


class AwardDivisionException(BaseException):
    pass


class Values(BasicEntity):
    def __init__(self, red_bet_sizes,
                 gold_bet_sizes,
                 max_players_team,
                 time_to_check_championship_viability: int,
                 championship_award_first_place_perc: int,
                 championship_award_second_place_perc: int,
                 championship_award_third_place_perc: int,
                 interval_between_championship_levels: int,
                 validator_maps: [ValidatorMaps],
                 entity_id: str = None):
        super(Values, self).__init__(entity_id=entity_id)
        self.red_bet_sizes = red_bet_sizes
        self.gold_bet_sizes = gold_bet_sizes
        self.max_players_team = max_players_team
        self.time_to_check_championship_viability = \
            time_to_check_championship_viability
        self.championship_award_first_place_perc = \
            championship_award_first_place_perc
        self.championship_award_second_place_perc = \
            championship_award_second_place_perc
        self.championship_award_third_place_perc = \
            championship_award_third_place_perc
        self.interval_between_championship_levels = \
            interval_between_championship_levels
        self.validator_maps = validator_maps

        self.check_championship_award_values()
        self.validate_championship_award_division()

    def validate_championship_award_division(self):
        first_award = self.championship_award_first_place_perc
        second_award = self.championship_award_second_place_perc
        third_award = self.championship_award_third_place_perc

        division_sum = first_award + second_award + third_award
        if division_sum != 100:
            raise AwardDivisionException(f'Awards has to sum 100, '
                                         f'but the sum is {division_sum}')

        if (first_award < second_award) or (first_award < third_award):
            raise AwardDivisionException(
                'First tournament place award cannot be less than '
                'second place or third place award')
        if second_award < third_award:
            raise AwardDivisionException(
                'Second tournament place award cannot be less than '
                'third place award')

    def check_championship_award_values(self):
        if self.championship_award_first_place_perc < 1:
            raise AwardDivisionException(
                'First tournament place award cannot be zero or negative')
        if self.championship_award_second_place_perc < 0:
            raise AwardDivisionException(
                'Second tournament place award cannot be negative')
        if self.championship_award_third_place_perc < 0:
            raise AwardDivisionException(
                'Third tournament place award cannot be negative')
        return True

    class Schema(BasicEntity.Schema):
        red_bet_sizes = fields.List(fields.Integer, many=True, required=True)
        gold_bet_sizes = fields.List(fields.Integer, many=True, required=True)
        max_players_team = fields.Integer(required=True)
        time_to_check_championship_viability = fields.Integer(
            required=False, allow_none=True, default=60, missing=60)
        championship_award_first_place_perc = fields.Integer(
            required=False, allow_none=True, default=70, missing=70)
        championship_award_second_place_perc = fields.Integer(
            required=False, allow_none=True, default=20, missing=20)
        championship_award_third_place_perc = fields.Integer(
            required=False, allow_none=True, default=10, missing=10)
        interval_between_championship_levels = fields.Integer(
            required=False, allow_none=True, default=30, missing=30)
        validator_maps = fields.Nested(
            ValidatorMaps.Schema, required=False, missing=[], default=[],
            many=True)

        @post_load
        def post_load(self, data, many, partial):
            return Values(**data)
