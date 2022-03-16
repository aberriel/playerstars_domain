from marshmallow import post_load
from . import Tournament


class TeamTournament(Tournament):
    def __init__(self,
                 game,
                 console,
                 award_first_place_perc,
                 award_second_place_perc,
                 award_third_place_perc,
                 price_to_enter,
                 member_amount,
                 level_duration,
                 levels_per_day,
                 start_datetime,
                 members,
                 status,
                 creation_datetime,
                 phases=None,
                 entity_id=None):
        super(TeamTournament, self).__init__(
            entity_id=entity_id,
            game=game,
            console=console,
            award_first_place_perc=award_first_place_perc,
            award_second_place_perc=award_second_place_perc,
            award_third_place_perc=award_third_place_perc,
            price_to_enter=price_to_enter,
            member_amount=member_amount,
            level_duration=level_duration,
            levels_per_day=levels_per_day,
            start_datetime=start_datetime,
            members=members,
            phases=phases,
            status=status,
            creation_datetime=creation_datetime)

    def is_member(self, player_id):
        self.logger.info('TEAM TOURNAMENT')
        pass

    class Schema(Tournament.Schema):

        @post_load
        def post_load(self, data, many, partial):
            return TeamTournament(**data)
