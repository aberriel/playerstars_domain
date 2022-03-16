from uuid import uuid4

from pytest import raises

from playerstars_domain import (
    MemberStatus,
    MemberType,
    Team,
    TeamMember)
from playerstars_domain.team.team import MemberNotFoundException
from tests.util import (
    captain,
    member_list_with_2,
    player_1,
    player_2,
    player_3,
    player_4,
    player_5,
    player_6)
from tests.util import generic_serialize_roundtrip_test


def make_team_data():
    captain_data = captain()
    members = member_list_with_2()
    team = Team(name='Brazucas',
                captain=captain_data,
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                game_id='05a5dd62-50af-43f7-aed5-9e1df17437cc',
                members=members,
                description='testinho')
    return team


def test_team_member():
    member_data = TeamMember(player_id=player_1().entity_id)
    assert member_data
    assert member_data.member_type == MemberType.MEMBER
    assert member_data.status == MemberStatus.INVITED
    assert member_data.last_status_change_datetime


def test_team_member_change_status():
    member_data = TeamMember(player_1().entity_id)
    initial_last_status_change = member_data.last_status_change_datetime
    assert member_data.status == MemberStatus.INVITED

    member_data.change_status(MemberStatus.ACCEPTED)
    assert member_data.status == MemberStatus.ACCEPTED
    assert member_data.last_status_change_datetime != \
        initial_last_status_change


def test_team_member_change_status_for_rejected_invite():
    member_data = TeamMember(player_id=player_1().entity_id,
                             member_type=MemberType.MEMBER,
                             status=MemberStatus.REJECTED)
    with raises(Exception) as exc:
        member_data.change_status(MemberStatus.REJECTED)
    assert 'The member has already rejected the invitation' in str(exc.value)


def test_team_member_change_status_for_initial_gone_out():
    member_data = TeamMember(player_id=player_1().entity_id,
                             member_type=MemberType.MEMBER,
                             status=MemberStatus.GONE_OUT)
    with raises(Exception) as exc:
        member_data.change_status(MemberStatus.REJECTED)
    assert 'The member has already left the team' in str(exc.value)


def test_team_member_reject_invite_for_captain():
    member_data = TeamMember(player_id=player_1().entity_id,
                             member_type=MemberType.CAPTAIN,
                             status=MemberStatus.ACCEPTED)
    with raises(Exception) as exc:
        member_data.change_status(MemberStatus.REJECTED)
    assert 'Captain cannot leave the team' in str(exc.value)


def test_team_member_leave_for_captain():
    member_data = TeamMember(player_id=player_1().entity_id,
                             member_type=MemberType.CAPTAIN,
                             status=MemberStatus.ACCEPTED)
    with raises(Exception) as exc:
        member_data.change_status(MemberStatus.GONE_OUT)
    assert 'Captain cannot leave the team' in str(exc.value)


def test_team():
    member_list = member_list_with_2()
    captain_data = captain()
    team = Team(name='Brazucas',
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                game_id="schrubles",
                captain=captain_data,
                members=member_list)

    assert team
    assert len(team.members) == 3
    assert captain_data in team.members
    assert team.captain.player_id == captain_data.player_id
    assert team.members[0].player_id == member_list[0].player_id


def test_team_add_game_points():
    team_data = make_team_data()
    assert team_data
    assert team_data.victories == 0

    team_data.add_game_point()
    assert team_data.victories == 1
    team_data.add_game_point()
    assert team_data.victories == 2


def test_team_add_member():
    member_list = member_list_with_2()
    player_4_data = player_4()
    team = Team(name='Brazucas',
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                captain=captain(),
                members=member_list)
    assert len(team.members) == 3

    add_result = team.add_member(player=player_4_data)
    assert add_result
    assert len(team.members) == 4

    member_found: TeamMember = \
        next((x for x in team.members if x.player_id == player_4_data.entity_id), None)
    assert member_found
    assert member_found.association_date


def test_team_add_member_accepted():
    member_list = member_list_with_2
    player_4_data = player_4()
    team = Team(name='Brazucas',
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                captain=captain(),
                members=member_list())

    with raises(Exception) as exc:
        team.add_member(
            player=player_4_data,
            member_type=MemberType.MEMBER,
            initial_status=MemberStatus.ACCEPTED)
    assert 'Members can only be added as invited' in str(exc.value)


def test_team_add_captain_as_not_accepted():
    member_list = member_list_with_2
    captain_data = captain()
    player_1_data = player_1()
    team = Team(name='Brazucas',
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                captain=captain_data,
                members=member_list())

    new_member_list = [x for x in team.members
                       if x.player_id != captain_data.player_id]
    team.members = new_member_list

    with raises(Exception) as exc:
        team.add_member(
            player=player_1_data,
            member_type=MemberType.CAPTAIN,
            initial_status=MemberStatus.REJECTED)
    assert 'The captain can only be added as member' in str(exc.value)


def test_team_add_member_already_added():
    member_list = member_list_with_2
    player_2_data = player_2()

    team = Team(name='Brazucas',
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                captain=captain(),
                members=member_list())
    assert len(team.members) == 3

    add_result = team.add_member(player=player_2_data)
    assert not add_result
    assert len(team.members) == 3


def test_remove_member():
    team = make_team_data()
    member_rogerio = next((x for x in team.members if x.player_id == 'abc123'),
                          None)
    assert member_rogerio
    assert len(team.members) == 3

    delete_result = team.remove_member('abc123')
    assert delete_result
    assert team.members is not None
    assert len(team.members) == 2


def test_remove_member_not_exists():
    team = make_team_data()
    random_id = str(uuid4())
    delete_result = team.remove_member(random_id)

    assert not delete_result
    assert team.members is not None
    assert len(team.members) == 3


def test_try_to_remove_captain():
    team = make_team_data()
    player_1_data = player_1()
    with raises(Exception) as exc:
        team.remove_member(player_1_data.entity_id)
    assert "You can't remove captain" in str(exc.value)


def test_find_member_by_id_member():
    team = make_team_data()
    player_2_data = player_2()
    member_found = team.find_member_by_id(player_2_data.entity_id)
    assert member_found
    assert member_found.member_type == MemberType.MEMBER
    assert member_found.player_id == player_2_data.entity_id


def test_find_member_by_id_captain():
    team = make_team_data()
    player_1_data = player_1()
    member_found = team.find_member_by_id(player_1_data.entity_id)
    assert member_found
    assert member_found.member_type == MemberType.CAPTAIN
    assert member_found.player_id == player_1_data.entity_id


def test_find_member_not_found():
    team = make_team_data()
    player_6_data = player_6()
    with raises(MemberNotFoundException):
        team.find_member_by_id(player_6_data.entity_id)


def test_leave_team():
    player_2_data = player_2()
    player_3_data = player_3()
    member_1 = TeamMember(player_id=player_2_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.ACCEPTED)
    member_2 = TeamMember(player_id=player_3_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.INVITED)
    member_list = [member_1, member_2]

    team = Team(name='Brazucas',
                captain=captain(),
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                members=member_list,
                description='testinho')
    all_active_members = team.get_active_members()
    assert len(all_active_members) == 2

    team.leave_team(player_2_data.entity_id)
    all_active_members_later = team.get_active_members()
    assert len(all_active_members_later) == 1

    with raises(MemberNotFoundException):
        team.find_member_by_id(player_2_data.entity_id)


def test_leave_team_captain():
    member_1 = TeamMember(player_id=player_2().entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.ACCEPTED)
    member_2 = TeamMember(player_id=player_3().entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.INVITED)
    member_list = [member_1, member_2]

    captain_data = captain()
    team = Team(name='Brazucas',
                captain=captain_data,
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                members=member_list,
                description='testinho')

    with raises(Exception) as exc:
        team.leave_team(captain_data.player_id)
    assert "Captain can't be removed" in str(exc.value)


def test_leave_not_member():
    member_1 = TeamMember(player_id=player_2().entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.ACCEPTED)
    member_2 = TeamMember(player_id=player_3().entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.INVITED)
    member_list = [member_1, member_2]

    player_6_data = player_6()
    team = Team(name='Brazucas',
                captain=captain(),
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                members=member_list,
                description='testinho')

    with raises(Exception) as exc:
        team.leave_team(player_6_data.entity_id)
    assert "The player isn't member of this team" in str(exc.value)


def test_leave_rejected():
    player_2_data = player_2()
    player_3_data = player_3()
    member_1 = TeamMember(player_id=player_2_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.REJECTED)
    member_2 = TeamMember(player_id=player_3_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.INVITED)
    member_list = [member_1, member_2]

    team = Team(name='Brazucas',
                captain=captain(),
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                members=member_list,
                description='testinho')

    with raises(Exception) as exc:
        team.leave_team(player_2_data.entity_id)
    assert 'The member cannot leave because your status is REJECTED' \
           in str(exc.value)

    member_found = team.find_member_by_id(player_2_data.entity_id)
    assert member_found
    assert member_found.status == MemberStatus.REJECTED


def test_leave_member_only_invited():
    player_2_data = player_2()
    player_3_data = player_3()
    member_1 = TeamMember(player_id=player_2_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.ACCEPTED)
    member_2 = TeamMember(player_id=player_3_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.INVITED)
    member_list = [member_1, member_2]

    team = Team(name='Brazucas',
                captain=captain(),
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                members=member_list,
                description='testinho')

    with raises(Exception) as exc:
        team.leave_team(player_3_data.entity_id)
    assert 'The member cannot leave because your status is INVITED' \
           in str(exc.value)

    member_found = team.find_member_by_id(player_3_data.entity_id)
    assert member_found
    assert member_found.status == MemberStatus.INVITED


def test_accept_invite():
    player_2_data = player_2()
    player_3_data = player_3()
    member_1 = TeamMember(player_id=player_2_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.INVITED)
    member_2 = TeamMember(player_id=player_3_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.INVITED)
    member_list = [member_1, member_2]

    team = Team(name='Brazucas',
                captain=captain(),
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                members=member_list,
                description='testinho')
    active_members_before = team.get_active_members()
    assert len(active_members_before) == 1

    team.member_invite_response(
        player_id=player_2_data.entity_id,
        accept=True)
    active_members_after = team.get_active_members()

    assert len(active_members_after) == 2
    member_found = team.find_member_by_id(player_2_data.entity_id)
    assert member_found
    assert member_found.status == MemberStatus.ACCEPTED


def test_reject_invite():
    player_2_data = player_2()
    player_3_data = player_3()
    member_1 = TeamMember(player_id=player_2_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.INVITED)
    member_2 = TeamMember(player_id=player_3_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.INVITED)
    member_list = [member_1, member_2]

    team = Team(name='Brazucas',
                captain=captain(),
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                members=member_list,
                description='testinho')

    team.member_invite_response(
        player_id=player_2_data.entity_id,
        accept=False)
    active_members = team.get_active_members()
    assert len(active_members) == 1
    member_found = team.find_member_by_id(player_2_data.entity_id)
    assert member_found
    assert member_found.status == MemberStatus.REJECTED


def test_accept_invite_not_member():
    player_2_data = player_2()
    player_3_data = player_3()
    player_5_data = player_5()
    member_1 = TeamMember(player_id=player_2_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.INVITED)
    member_2 = TeamMember(player_id=player_3_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.INVITED)
    member_list = [member_1, member_2]

    team = Team(name='Brazucas',
                captain=captain(),
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                members=member_list,
                description='testinho')

    with raises(Exception) as exc:
        team.member_invite_response(
            player_id=player_5_data.entity_id,
            accept=True)
    assert "The player isn't member of this team" in str(exc.value)


def test_accept_invite_team_full():
    player_2_data = player_2()
    player_3_data = player_3()
    player_4_data = player_4()
    player_5_data = player_5()
    player_6_data = player_6()
    member_1 = TeamMember(player_id=player_2_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.ACCEPTED)
    member_2 = TeamMember(player_id=player_3_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.ACCEPTED)
    member_3 = TeamMember(player_id=player_4_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.ACCEPTED)
    member_4 = TeamMember(player_id=player_5_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.ACCEPTED)
    member_5 = TeamMember(player_id=player_6_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.INVITED)
    member_list = [member_1, member_2, member_3, member_4, member_5]

    team = Team(name='Brazucas',
                captain=captain(),
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                members=member_list,
                description='testinho')
    active_members_before = team.get_active_members()
    assert len(active_members_before) == 5

    with raises(Exception) as exc:
        team.member_invite_response(
            player_id=player_6_data.entity_id,
            accept=True)
    assert 'The team Brazucas is full' in str(exc.value)


def test_accept_invite_already_rejected():
    player_2_data = player_2()
    player_3_data = player_3()
    member_1 = TeamMember(player_id=player_2_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.REJECTED)
    member_2 = TeamMember(player_id=player_3_data.entity_id,
                          member_type=MemberType.MEMBER,
                          status=MemberStatus.INVITED)
    member_list = [member_1, member_2]

    team = Team(name='Brazucas',
                captain=captain(),
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                members=member_list,
                description='testinho')

    with raises(Exception) as exc:
        team.member_invite_response(
            player_id=player_2_data.entity_id,
            accept=True)
    assert 'The member cannot accept the invite ' \
           'because he rejected the invitation' in str(exc.value)


def test_accept_invite_as_captain():
    member_list = member_list_with_2()
    captain_data = captain()
    team = Team(name='Brazucas',
                captain=captain(),
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                members=member_list,
                description='testinho')

    with raises(Exception) as exc:
        team.member_invite_response(
            player_id=captain_data.player_id,
            accept=True)
    assert "Captain can't accept invitation" in str(exc.value)


def test_check_if_member():
    team = Team(name='Brazucas',
                captain=captain(),
                console_id='308995bd-6c03-4a60-be06-c599df86a384',
                members=member_list_with_2(),
                description='testinho')
    assert team.check_if_member('q1w2e3')


def test_team_roundtrip():
    team_data = make_team_data()
    generic_serialize_roundtrip_test(Team, team_data)
