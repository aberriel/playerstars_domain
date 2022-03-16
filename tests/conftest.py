import json

from pytest import fixture

from playerstars_domain import Player


@fixture
def player():
    with open('tests/fixtures/player.json', 'r') as f:
        return Player.from_json(json.load(f))
