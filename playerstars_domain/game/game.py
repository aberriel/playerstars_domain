from clapy_basic_classes import BasicEntity
from enum import Enum
from marshmallow import fields, post_load
from marshmallow_enum import EnumField


class GameType(Enum):
    INDIVIDUAL = 'INDIVIDUAL'
    COLLECTIVE = 'COLLECTIVE'
    BOTH = 'BOTH'


class Game(BasicEntity):
    def __init__(self,
                 name: str,
                 logo_path: str,
                 entity_id: str = None,
                 victories: int = 0,
                 points: int = 0,
                 tutorial: str = None,
                 game_type: GameType = GameType.BOTH,
                 mask: str = None,
                 active: bool = False):
        super(Game, self).__init__(entity_id=entity_id)
        self.name = name
        self.logo_path = logo_path
        self.points = points
        self.victories = victories
        self.tutorial = tutorial
        self.game_type = game_type
        self.mask = mask
        self.active = active

    def __repr__(self):
        return self.name

    class Schema(BasicEntity.Schema):
        OPTIONAL_INT = dict(required=False, allow_none=False, default=0,
                            missing=0)

        name = fields.String(required=True, allow_none=False)
        logo_path = fields.String(required=True)
        points = fields.Integer(**OPTIONAL_INT)
        victories = fields.Integer(**OPTIONAL_INT)
        tutorial = fields.String(required=False, allow_none=True)
        mask = fields.String(required=False, allow_none=True)
        game_type = EnumField(
            GameType,
            required=False,
            allow_none=False,
            default=GameType.BOTH,
            missing=GameType.BOTH)
        active = fields.Boolean(
            required=False,
            allow_none=True,
            default=False,
            missing=False)

        @post_load
        def post_load(self, data, many, partial):
            return Game(**data)
