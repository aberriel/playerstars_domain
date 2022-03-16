from clapy_basic_classes.basic_domain.util import generic_serialize_roundtrip_test
from datetime import datetime
from playerstars_domain import (
    Game,
    GameType,
    PlayerTournament,
    Tournament,
    TournamentMember, TournamentMemberStatus, TournamentStatus,
    TeamTournament, TournamentPhase)
from playerstars_domain.utils.datetime_helper import aware_utc, aware_now
from unittest.mock import MagicMock, patch


def tournament():
    game = Game(
        name='Sonic',
        logo_path='/images/sonic.png',
        entity_id='game123',
        victories=0,
        points=0,
        tutorial=None,
        game_type=GameType.BOTH)
    console = MagicMock()
    # noinspection PyTypeChecker
    members = [TournamentMember(f'id{i}', s) for i, s in enumerate(TournamentMemberStatus)]
    phases = [TournamentPhase(
        duels=['duel1', 'duel2', 'duel3'],
        phase=TournamentStatus.PHASE1,
        start_datetime=aware_now()
    )]
    tournament = Tournament(
        game=game,
        console=console,
        award_first_place_perc=70,
        award_second_place_perc=25,
        award_third_place_perc=5,
        price_to_enter=42,
        member_amount=16,
        level_duration=300,
        levels_per_day=2,
        start_datetime=aware_utc(datetime(2020, 1, 1, 14, 20)),
        members=members,
        phases=phases,
        status=TournamentStatus.WAITING_START,
        creation_datetime=aware_utc(datetime(2020, 1, 1, 8, 0)))
    return tournament


@patch('clapy_basic_classes.basic_domain.basic_entity.uuid4',
       return_value='f9684ac1-fe78-497f-a4af-ff040c89a84d')
def test_tournament(mock_uuid4):
    _tournament = tournament()
    assert not _tournament.is_member('123')
    assert _tournament.entity_id == mock_uuid4.return_value
    generic_serialize_roundtrip_test(Tournament, _tournament)


@patch('clapy_basic_classes.basic_domain.basic_entity.uuid4',
       return_value='f9684ac1-fe78-497f-a4af-ff040c89a84d')
def test_player_tournament(mock_uuid4):
    _tournament = tournament()
    assert _tournament.entity_id == mock_uuid4.return_value
    generic_serialize_roundtrip_test(PlayerTournament, _tournament)


@patch('clapy_basic_classes.basic_domain.basic_entity.uuid4',
       return_value='f9684ac1-fe78-497f-a4af-ff040c89a84d')
def test_team_tournament(mock_uuid4):
    _tournament = tournament()
    assert _tournament.entity_id == mock_uuid4.return_value
    generic_serialize_roundtrip_test(TeamTournament, _tournament)


def test_is_member():
    player_tournament = PlayerTournament(
        game=MagicMock(),
        console=MagicMock(),
        award_first_place_perc=70,
        award_second_place_perc=25,
        award_third_place_perc=5,
        price_to_enter=42,
        member_amount=16,
        level_duration=300,
        levels_per_day=2,
        start_datetime=aware_utc(datetime(2020, 1, 1, 14, 20)),
        members=[TournamentMember(f'id{i}', s) for i, s in enumerate(TournamentMemberStatus)],
        status=TournamentStatus.WAITING_START,
        creation_datetime=aware_utc(datetime(2020, 1, 1, 8, 0)))

    assert player_tournament.is_member('id0')


def test_team_tournament_init():
    team_tournament = TeamTournament(**tournament().to_json())
    assert team_tournament
    assert not team_tournament.is_member('123')


def test_tournament_properties():
    _tournament = tournament()
    assert _tournament.star_amount == 42 * 16
    assert _tournament.phases_amount == 4
    assert _tournament.finish_datetime == aware_utc(
        datetime(2020, 1, 5, 14, 20))
    assert _tournament.finish_date == "05/01/2020"
    assert _tournament.finish_time == "14:20:00"
    assert _tournament.confirmed_members == 2
    assert _tournament.first_place_prize == 42 * 16 * 70 / 100
    assert _tournament.second_place_prize == 42 * 16 * 25 / 100
    assert _tournament.third_place_prize == 42 * 16 * 5 / 100
    assert _tournament.creator_id == 'id3'
    _tournament.phases[0].set_logger(MagicMock())
    assert _tournament.phases[0].logger
