from clapy_basic_classes import BasicValue
from marshmallow import fields, post_load


class GamePoints(BasicValue):
    def __init__(self, game_id, victories=0,
                 elo_rating: float = 1500):
        super(GamePoints, self).__init__()
        self.game_id = game_id
        self.victories = victories
        self.elo_rating = elo_rating

    class Schema(BasicValue.Schema):
        game_id = fields.String(required=True, allow_none=False)
        victories = fields.Int(
            required=False,
            allow_none=True,
            missing=0,
            default=0)
        elo_rating = fields.Float(required=False,
                                  allow_none=False,
                                  default=1500,
                                  missing=1500)

        @post_load
        def post_load(self, data, many, partial):
            return GamePoints(**data)
