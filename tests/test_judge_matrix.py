from playerstars_domain import (
    DuelComponentResult,
    DuelJudgeResult,
    DuelReportState,
    ImageValidity,
    Inform,
    JudgeMatrix,
    PlayerDuelInfo)
from playerstars_domain.duel.duel_result import ComponentResult
from pytest import fixture
from unittest.mock import MagicMock


@fixture
def coded_matrix():
    return '''\
        I
        1X
        12I
        122I
        2222X
        22221I
        222211I
        TXTTXTTT
        T2II1ITTT
        T2TI11ITTT'''


@fixture
def expected_matrix():
    inp = DuelReportState
    out = DuelJudgeResult

    return {
        inp.NOT_INFORMED: {
            inp.NOT_INFORMED: out.INVALIDATED
        },
        inp.WIN_VALID: {
            inp.NOT_INFORMED: out.PLAYER1_WIN,
            inp.WIN_VALID: None
        },
        inp.WIN_INVALID: {
            inp.NOT_INFORMED: out.PLAYER1_WIN,
            inp.WIN_VALID: out.PLAYER2_WIN,
            inp.WIN_INVALID: out.INVALIDATED
        },
        inp.WIN_NOT_SENT: {
            inp.NOT_INFORMED: out.PLAYER1_WIN,
            inp.WIN_VALID: out.PLAYER2_WIN,
            inp.WIN_INVALID: out.PLAYER2_WIN,
            inp.WIN_NOT_SENT: out.INVALIDATED
        },
        inp.LOSS_VALID: {
            inp.NOT_INFORMED: out.PLAYER2_WIN,
            inp.WIN_VALID: out.PLAYER2_WIN,
            inp.WIN_INVALID: out.PLAYER2_WIN,
            inp.WIN_NOT_SENT: out.PLAYER2_WIN,
            inp.LOSS_VALID: None
        },
        inp.LOSS_INVALID: {
            inp.NOT_INFORMED: out.PLAYER2_WIN,
            inp.WIN_VALID: out.PLAYER2_WIN,
            inp.WIN_INVALID: out.PLAYER2_WIN,
            inp.WIN_NOT_SENT: out.PLAYER2_WIN,
            inp.LOSS_VALID: out.PLAYER1_WIN,
            inp.LOSS_INVALID: out.INVALIDATED
        },
        inp.LOSS_NOT_SENT: {
            inp.NOT_INFORMED: out.PLAYER2_WIN,
            inp.WIN_VALID: out.PLAYER2_WIN,
            inp.WIN_INVALID: out.PLAYER2_WIN,
            inp.WIN_NOT_SENT: out.PLAYER2_WIN,
            inp.LOSS_VALID: out.PLAYER1_WIN,
            inp.LOSS_INVALID: out.PLAYER1_WIN,
            inp.LOSS_NOT_SENT: out.INVALIDATED
        },
        inp.TIE_VALID: {
            inp.NOT_INFORMED: out.TIED,
            inp.WIN_VALID: None,
            inp.WIN_INVALID: out.TIED,
            inp.WIN_NOT_SENT: out.TIED,
            inp.LOSS_VALID: None,
            inp.LOSS_INVALID: out.TIED,
            inp.LOSS_NOT_SENT: out.TIED,
            inp.TIE_VALID: out.TIED
        },
        inp.TIE_INVALID: {
            inp.NOT_INFORMED: out.TIED,
            inp.WIN_VALID: out.PLAYER2_WIN,
            inp.WIN_INVALID: out.INVALIDATED,
            inp.WIN_NOT_SENT: out.INVALIDATED,
            inp.LOSS_VALID: out.PLAYER1_WIN,
            inp.LOSS_INVALID: out.INVALIDATED,
            inp.LOSS_NOT_SENT: out.TIED,
            inp.TIE_VALID: out.TIED,
            inp.TIE_INVALID: out.TIED
        },
        inp.TIE_NOT_SENT: {
            inp.NOT_INFORMED: out.TIED,
            inp.WIN_VALID: out.PLAYER2_WIN,
            inp.WIN_INVALID: out.TIED,
            inp.WIN_NOT_SENT: out.INVALIDATED,
            inp.LOSS_VALID: out.PLAYER1_WIN,
            inp.LOSS_INVALID: out.PLAYER1_WIN,
            inp.LOSS_NOT_SENT: out.INVALIDATED,
            inp.TIE_VALID: out.TIED,
            inp.TIE_INVALID: out.TIED,
            inp.TIE_NOT_SENT: out.TIED
        }
    }


def test_get_inform_from_component_result():
    result_0 = None
    inform_0 = Inform.get_inform_from_component_result(result_0)
    assert inform_0 == Inform.NONE

    result_1 = DuelComponentResult(result=ComponentResult.WINNER)
    inform_1 = Inform.get_inform_from_component_result(result_1)
    assert inform_1 == Inform.WIN

    result_2 = DuelComponentResult(result=ComponentResult.LOSER)
    inform_2 = Inform.get_inform_from_component_result(result_2)
    assert inform_2 == Inform.LOSS

    result_3 = DuelComponentResult(result=ComponentResult.TIED)
    inform_3 = Inform.get_inform_from_component_result(result_3)
    assert inform_3 == Inform.TIE

    result_4 = DuelComponentResult(result=ComponentResult.RESIGNED)
    inform_4 = Inform.get_inform_from_component_result(result_4)
    assert inform_4 == Inform.RES


def test_get_player_duel_info_win_valid():
    result = DuelComponentResult(
        result=ComponentResult.WINNER,
        result_image='images/result.jpg')
    duel_info = PlayerDuelInfo.get_player_duel_info(result, ImageValidity.VALID)
    assert duel_info.report_state == DuelReportState.WIN_VALID


def test_get_player_duel_info_loss_invalid():
    result = DuelComponentResult(
        result=ComponentResult.LOSER,
        result_image='images/result.jpg')
    duel_info = PlayerDuelInfo.get_player_duel_info(result, ImageValidity.INVALID)
    assert duel_info.report_state == DuelReportState.LOSS_INVALID


def test_get_player_duel_info_tie_valid():
    result = DuelComponentResult(
        result=ComponentResult.TIED,
        result_image='images/result.jpg')
    duel_info = PlayerDuelInfo.get_player_duel_info(result, ImageValidity.VALID)
    assert duel_info.report_state == DuelReportState.TIE_VALID


def test_get_player_duel_info_tie_not_sent():
    result = DuelComponentResult(ComponentResult.TIED)
    duel_info = PlayerDuelInfo.get_player_duel_info(result, ImageValidity.NOT_SENT)
    assert duel_info.report_state == DuelReportState.TIE_NOT_SENT


def test_get_player_duel_info_not_informed():
    duel_info = PlayerDuelInfo.get_player_duel_info()
    assert duel_info.report_state == DuelReportState.NOT_INFORMED


# noinspection PyProtectedMember
def test_judge_matrix_decode(coded_matrix, expected_matrix):
    jm = JudgeMatrix(MagicMock(), MagicMock(), coded_matrix)
    matrix = jm._configure_judge_matrix(DuelJudgeResult.PLAYER1_WIN,
                                        DuelJudgeResult.PLAYER2_WIN)
    assert matrix == expected_matrix


def test_player_duel_info():
    pdi = PlayerDuelInfo(Inform.WIN, ImageValidity.VALID)
    assert pdi.report_state == DuelReportState.WIN_VALID


def test_judge_p1_win(coded_matrix):
    p1i = PlayerDuelInfo(Inform.WIN, ImageValidity.VALID)
    p2i = PlayerDuelInfo(Inform.LOSS, ImageValidity.VALID)
    jm = JudgeMatrix(p1i, p2i, coded_matrix)
    assert jm.judge_result() == DuelJudgeResult.PLAYER1_WIN


def test_judge_p2_win(coded_matrix):
    p1i = PlayerDuelInfo(Inform.LOSS, ImageValidity.VALID)
    p2i = PlayerDuelInfo(Inform.WIN, ImageValidity.VALID)
    jm = JudgeMatrix(p1i, p2i, coded_matrix)
    assert jm.judge_result() == DuelJudgeResult.PLAYER2_WIN


def test_judge_expired(coded_matrix):
    p1i = PlayerDuelInfo(Inform.NONE, ImageValidity.NOT_SENT)
    p2i = PlayerDuelInfo(Inform.NONE, ImageValidity.NOT_SENT)
    jm = JudgeMatrix(p1i, p2i, coded_matrix)
    assert jm.judge_result() == DuelJudgeResult.INVALIDATED


def test_judge_tied(coded_matrix):
    p1i = PlayerDuelInfo(Inform.TIE, ImageValidity.VALID)
    p2i = PlayerDuelInfo(Inform.TIE, ImageValidity.NOT_SENT)
    jm = JudgeMatrix(p1i, p2i, coded_matrix)
    assert jm.judge_result() == DuelJudgeResult.TIED


def test_judge_impossivel(coded_matrix):
    p1i = PlayerDuelInfo(Inform.WIN, ImageValidity.VALID)
    p2i = PlayerDuelInfo(Inform.WIN, ImageValidity.VALID)
    jm = JudgeMatrix(p1i, p2i, coded_matrix)
    assert jm.judge_result() is None
