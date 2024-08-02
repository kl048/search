import random
from otree.api import *

doc = """
Comparing Single Search and Joint Search
Basic Job Search
- Subject starts with an endowment (outside option) of 20 ECUs
- Subject sets reservation wage r 
- Each period an unemployed subject receives an offer with probability 0.50
- Wage offer, w, drawn from U[1,100]
- If w >= r subject becomes employed
- If subject is employed when game ends then earn w, otherwise earn 0 (in addition to the endowment)
- Another period occurs with probability 0.95
Three Treatments: Individual, Chat, Team
"""

class C(BaseConstants):
    NAME_IN_URL = 'search_experiment'
    PLAYERS_PER_GROUP = None  # Dynamic definition
    NUM_ROUNDS = 20
    ENDOWMENT = cu(20)
    ALPHA = 0.5
    THETA = 100
    DELTA = 0.95
    CHAT_DURATION_LONG = 60
    CHAT_DURATION_SHORT = 30
    EXCHANGE_RATE = 0.1
    SHOW_UP_FEE = 7
    ECU_LABEL = 'ECUs'

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    session = subsession.session
    players_per_group = session.config['players_per_group']
    num_participants = session.num_participants

    if num_participants % players_per_group != 0:
        raise ValueError('Number of participants must be a multiple of players_per_group')

    players = subsession.get_players()
    group_matrix = [players[i:i + players_per_group] for i in range(0, len(players), players_per_group)]

    subsession.set_group_matrix(group_matrix)
    for player in players:
        player.treatment = session.config['treatment']
        player.endowment = C.ENDOWMENT
        player.is_employed = False
        player.round_payoff = 0

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    treatment = models.StringField()
    reservation_wage = models.IntegerField(
        min=0,
        max=C.THETA,
        label="Set your reservation wage"
    )
    wage_offer = models.IntegerField(blank=True)
    accepted = models.BooleanField(initial=False)
    earnings = models.CurrencyField()
    is_employed = models.BooleanField(initial=False)
    round_payoff = models.CurrencyField()
    total_earnings = models.CurrencyField()
    chat_content = models.LongStringField(blank=True)
    endowment = models.CurrencyField(initial=C.ENDOWMENT)

def set_wage_offer(player: Player):
    if random.random() < C.ALPHA:
        player.wage_offer = random.randint(1, C.THETA)
    else:
        player.wage_offer = None

def set_earnings(player: Player):
    if player.field_maybe_none('wage_offer') is not None and player.wage_offer >= player.reservation_wage:
        player.accepted = True
        player.is_employed = True
        player.earnings = player.wage_offer
    else:
        player.accepted = False
        player.earnings = 0
    player.round_payoff = player.earnings + C.ENDOWMENT

def get_chat_duration(player: Player):
    return C.CHAT_DURATION_LONG if player.round_number < 5 else C.CHAT_DURATION_SHORT

def set_total_earnings(player: Player):
    selected_round = random.randint(1, C.NUM_ROUNDS)
    selected_round_payoff = player.in_round(selected_round).round_payoff
    player.total_earnings = selected_round_payoff * C.EXCHANGE_RATE + C.SHOW_UP_FEE

# Pages

class SetReservationWage(Page):
    form_model = 'player'
    form_fields = ['reservation_wage']

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.field_maybe_none('treatment')
        return {
            'round_number': player.round_number,
            'endowment': C.ENDOWMENT,
            'ecus': C.ECU_LABEL,
            'chat_group': f'chat_{player.group.id}' if treatment in ['C', 'T'] else None
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        set_wage_offer(player)
        set_earnings(player)


class WaitForAllPlayers(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment in ['C', 'T']

    wait_for_all_groups = True

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'reservation_wage': player.reservation_wage,
            'wage_offer': player.wage_offer if player.field_maybe_none('wage_offer') is not None else 'No offer',
            'accepted': player.accepted,
            'earnings': player.earnings
        }

class TeamResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'team_earnings': sum([p.earnings for p in player.group.get_players()]) / 2
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'T'

class FinalEarnings(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        set_total_earnings(player)
        player.participant.vars['total_earnings'] = player.total_earnings
        return {
            'selected_round': player.in_round(random.randint(1, C.NUM_ROUNDS)),
            'total_earnings': player.total_earnings,
            'show_up_fee': C.SHOW_UP_FEE,
            'conversion_rate': C.EXCHANGE_RATE,
        }


page_sequence = [
    SetReservationWage,
    WaitForAllPlayers,  # Ensure all players wait here to synchronize for Chat and Team treatments
    Results,
    TeamResults,
    FinalEarnings
]
