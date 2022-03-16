from clapy_basic_classes import BasicEntity
from marshmallow import fields, post_load
from playerstars_domain.game import Game, GameType
from typing import List


class GameNotFoundException(BaseException):
    pass


class Console(BasicEntity):
    def __init__(self,
                 name: str,
                 logo_path: str,
                 tag_name: str = None,
                 games: list = None,
                 entity_id: str = None):
        super(Console, self).__init__(entity_id=entity_id)
        self.name = name
        self.logo_path = logo_path
        self.tag_name = tag_name
        self.games: List[Game] = games if games else []
        self.game_list = ", ".join([str(x) for x in self.games])

    def find_game_by_id(self, game_id: str):
        try:
            return [x for x in self.games if x.entity_id == game_id][0]
        except IndexError:
            raise GameNotFoundException()

    def get_game_victories_by_id(self, game_id):
        try:
            return self.find_game_by_id(game_id).victories
        except GameNotFoundException:
            return None

    def get_individual_games(self):
        game_list = [x for x in self.games if x.game_type in [GameType.INDIVIDUAL, GameType.BOTH]]
        return game_list

    def get_collective_games(self):
        game_list = [x for x in self.games if x.game_type in [GameType.COLLECTIVE, GameType.BOTH]]
        return game_list

    def __repr__(self):
        return f'Console: {self.name}, Games: {self.game_list}'

    class Schema(BasicEntity.Schema):
        name = fields.String(required=True, allow_none=False)
        logo_path = fields.String(required=True)
        tag_name = fields.String(required=False, allow_none=True)
        games = fields.Nested(Game.Schema, many=True)

        @post_load
        def post_load(self, data, many, partial):
            return Console(**data)
