from enum import Enum
from playerstars_domain.duel.duel_result import ComponentResult


class DuelReportState(Enum):
    NOT_INFORMED = 'NOT_INFORMED'
    WIN_VALID = 'WIN_VALID'
    WIN_INVALID = 'WIN_INVALID'
    WIN_NOT_SENT = 'WIN_NOT_SENT'
    LOSS_VALID = 'LOSS_VALID'
    LOSS_INVALID = 'LOSS_INVALID'
    LOSS_NOT_SENT = 'LOSS_NOT_SENT'
    TIE_VALID = 'TIE_VALID'
    TIE_INVALID = 'TIE_INVALID'
    TIE_NOT_SENT = 'TIE_NOT_SENT'

    # noinspection PyTypeChecker
    def __lt__(self, other):
        self_index = list(DuelReportState).index(self)
        other_index = list(DuelReportState).index(other)
        return self_index < other_index


class Inform(Enum):
    WIN = "WIN"
    LOSS = "LOSS"
    TIE = "TIE"
    NONE = "NONE"
    RES = "RESIGNED"

    @classmethod
    def get_inform_from_component_result(cls, result=None):
        map = {
            ComponentResult.WINNER.value: Inform.WIN,
            ComponentResult.LOSER.value: Inform.LOSS,
            ComponentResult.TIED.value: Inform.TIE,
            ComponentResult.RESIGNED.value: Inform.RES
        }
        if not result:
            return Inform.NONE
        return map[result.result.value]


class ImageValidity(Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    NOT_SENT = "NOT_SENT"


class PlayerDuelInfo:
    def __init__(self,
                 inform: Inform = Inform.NONE,
                 image_validity: ImageValidity = ImageValidity.NOT_SENT):
        self.inform = inform
        self.image_validity = image_validity

    @property
    def report_state(self):
        drs = DuelReportState
        map_report = {
            (Inform.NONE, ImageValidity.NOT_SENT): drs.NOT_INFORMED,
            (Inform.WIN, ImageValidity.VALID): drs.WIN_VALID,
            (Inform.WIN, ImageValidity.INVALID): drs.WIN_INVALID,
            (Inform.WIN, ImageValidity.NOT_SENT): drs.WIN_NOT_SENT,
            (Inform.LOSS, ImageValidity.VALID): drs.LOSS_VALID,
            (Inform.LOSS, ImageValidity.INVALID): drs.LOSS_INVALID,
            (Inform.LOSS, ImageValidity.NOT_SENT): drs.LOSS_NOT_SENT,
            (Inform.TIE, ImageValidity.VALID): drs.TIE_VALID,
            (Inform.TIE, ImageValidity.INVALID): drs.TIE_INVALID,
            (Inform.TIE, ImageValidity.NOT_SENT): drs.TIE_NOT_SENT
        }
        return map_report[(self.inform, self.image_validity)]

    @classmethod
    def get_player_duel_info(cls, duel_member_result=None,
                             image_validation=ImageValidity.NOT_SENT):
        inform = Inform.get_inform_from_component_result(duel_member_result)
        return PlayerDuelInfo(inform, image_validation)


class DuelJudgeResult(Enum):
    PLAYER1_WIN = "PLAYER1_WIN"
    PLAYER2_WIN = "PLAYER2_WIN"
    TIED = "TIED"
    INVALIDATED = "INVALIDATED"


class JudgeMatrix:
    def __init__(self,
                 info_player_1: PlayerDuelInfo,
                 info_player_2: PlayerDuelInfo,
                 coded_matrix: str):
        """
        Julga o resultado de um duel de acordo com o que os jogadores
        informaram.
        :param info_player_1: Informação prestada pelo jogador 1
        :param info_player_2: Informação prestada pelo jogador 2
        :param coded_matrix: texto de configuração, onde:
            - cada linha contém os resultados da matriz
            - somente o triângulo inferior da grade é codificada
            - Os caracters para cada resultado são:
                I - Invalido
                1 - Player1 venceu
                2 - Player 2 venceu
                T - Empate
                X - Não atribuido (None)

            Exemplo:
            '''\
                I
                1X
                12I
                122I
                2X22X
                22221I
                222211I
                TXTTXTTT
                T2II1ITTT
                T2TI11ITTT'''
        """

        self.info_player_1 = info_player_1
        self.info_player_2 = info_player_2

        self.coded_matrix = coded_matrix

    # noinspection PyTypeChecker
    def _configure_judge_matrix(self,
                                player1_win: DuelJudgeResult,
                                player2_win: DuelJudgeResult):
        mtx_lines = [x.strip() for x in self.coded_matrix.split('\n')]
        result_map = {
            'I': DuelJudgeResult.INVALIDATED,
            'X': None,
            '1': player1_win,
            '2': player2_win,
            'T': DuelJudgeResult.TIED
        }

        matrix = {}
        for i, report in enumerate(DuelReportState):
            matrix[report] = {}
            for k, result in enumerate(list(mtx_lines[i])):
                matrix[report].update({
                    list(DuelReportState)[k]: result_map[result]})
        return matrix

    def _get_result(self,
                    win1: DuelJudgeResult,
                    win2: DuelJudgeResult,
                    p1: DuelReportState,
                    p2: DuelReportState) -> DuelJudgeResult:
        matrix = self._configure_judge_matrix(win1, win2)

        return matrix[p1][p2]

    def judge_result(self) -> DuelJudgeResult:
        player1_report = self.info_player_1.report_state
        player2_report = self.info_player_2.report_state

        if player2_report < player1_report:
            win1 = DuelJudgeResult.PLAYER1_WIN
            win2 = DuelJudgeResult.PLAYER2_WIN
            p1 = player1_report
            p2 = player2_report
        else:
            win1 = DuelJudgeResult.PLAYER2_WIN
            win2 = DuelJudgeResult.PLAYER1_WIN
            p1 = player2_report
            p2 = player1_report

        return self._get_result(win1, win2, p1, p2)
