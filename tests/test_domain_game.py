from playerstars_domain import Game, GameType
from uuid import uuid4

game = Game(name='fifa', logo_path='/user/fifa.png', game_type=GameType.BOTH, active=True)
game_id = game.entity_id


def test_game():
    assert game


def test_game_with_id():
    new_id = str(uuid4())
    new_game = Game(name='GTA V', logo_path='/images/gta5.png', entity_id=new_id)
    assert new_game
    assert new_game.entity_id == new_id


def test_game_repr():
    assert game.__repr__()
    assert game.__repr__() == 'fifa'


def test_game_attributes():
    assert game.entity_id == game_id
    assert game.name == 'fifa'
    assert game.logo_path == '/user/fifa.png'
    assert game.game_type == GameType.BOTH


def test_to_json():
    assert game.to_json() == dict(name='fifa',
                                  logo_path='/user/fifa.png',
                                  entity_id=game_id,
                                  points=0,
                                  victories=0,
                                  game_type='BOTH',
                                  tutorial=None,
                                  mask=None,
                                  active=True)


def test_from_json():
    json_data = dict(entity_id=str(uuid4()),
                     name='Super Mario',
                     logo_path='/images/mario.png',
                     game_type='BOTH')
    game = Game.from_json(json_data)
    assert game
    assert game.entity_id == json_data['entity_id']
    assert game.name == 'Super Mario'
    assert game.logo_path == '/images/mario.png'
    assert game.tutorial is None
    assert game.game_type == GameType.BOTH
    assert game.active is False
