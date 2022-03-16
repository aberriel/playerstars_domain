from . import Tournament
from marshmallow import post_load
import logging


class PlayerTournament(Tournament):
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
        super(PlayerTournament, self).__init__(
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
        self.logger = logging.getLogger(__name__)

    def is_member(self, player_id):
        self.logger.info('PLAYER TOURNAMENT')
        self.logger.info(player_id)
        member_id_list = [x.member_id for x in self.members]
        self.logger.info(member_id_list)
        return True if player_id in member_id_list else False

    class Schema(Tournament.Schema):

        @post_load
        def post_load(self, data, many, partial):
            return PlayerTournament(**data)
