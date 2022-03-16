from enum import Enum


class TournamentStatus(Enum):
    WAITING_START = 'WAITING_START'
    PHASE1 = 'PHASE1'
    PHASE2 = 'PHASE2'
    PHASE3 = 'PHASE3'
    PHASE4 = 'PHASE4'
    PHASE5 = 'PHASE5'
    RUNNING = 'RUNNING'
    FINISHED = 'FINISHED'
    CANCELED = 'CANCELED'
