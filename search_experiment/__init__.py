from otree.api import *

c = Currency

class Constants(BaseConstants):
    NAME_IN_URL = 'search_experiment'
    PLAYERS_PER_GROUP = 2  # Static definition to satisfy oTree checks
    NUM_ROUNDS = 20
    ENDOWMENT = c(20)
    ALPHA = 0.5
    THETA = 100
    DELTA = 0.95
    CHAT_DURATION_LONG = 60
    CHAT_DURATION_SHORT = 30
    EXCHANGE_RATE = 0.1
    SHOW_UP_FEE = 7

class Subsession(BaseSubsession):
    def creating_session(self):
        session = self.session
        players_per_group = session.config['players_per_group']
        num_participants = session.num_participants

        if num_participants % players_per_group != 0:
            raise ValueError('Number of participants must be a multiple of players_per_group')

        players = self.get_players()
        group_matrix = [players[i:i + players_per_group] for i in range(0, len(players), players_per_group)]

        self.set_group_matrix(group_matrix)
        for p in players:
            p.treatment = session.config['treatment']
            p.endowment = Constants.ENDOWMENT
            p.is_employed = False
            p.round_payoff = 0

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    treatment = models.StringField()
    reservation_wage = models.IntegerField(
        min=0,
        max=Constants.THETA,
        label="Set your reservation wage"
    )
    wage_offer = models.IntegerField()
    accepted = models.BooleanField(initial=False)
    earnings = models.CurrencyField()
    is_employed = models.BooleanField(initial=False)
    round_payoff = models.CurrencyField()
    total_earnings = models.CurrencyField()
    chat_content = models.LongStringField(blank=True)

    def set_wage_offer(self):
        if random.random() < Constants.ALPHA:
            self.wage_offer = random.randint(1, Constants.THETA)
        else:
            self.wage_offer = None

    def set_earnings(self):
        if self.wage_offer is not None and self.wage_offer >= self.reservation_wage:
            self.accepted = True
            self.is_employed = True
            self.earnings = self.wage_offer
        else:
            self.accepted = False
            self.earnings = 0
        self.round_payoff = self.earnings + Constants.ENDOWMENT

    def get_chat_duration(self):
        return Constants.CHAT_DURATION_LONG if self.round_number < 5 else Constants.CHAT_DURATION_SHORT

    def set_total_earnings(self):
        selected_round = random.randint(1, Constants.NUM_ROUNDS)
        selected_round_payoff = self.in_round(selected_round).round_payoff
        self.total_earnings = selected_round_payoff * Constants.EXCHANGE_RATE + Constants.SHOW_UP_FEE

# Pages

class SetReservationWage(Page):
    form_model = 'player'
    form_fields = ['reservation_wage']

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.field_maybe_none('treatment')
        return {
            'endowment': Constants.ENDOWMENT,
            'ecus': "ECUs",
            'chat_group': f'chat_{player.group.id}' if treatment in ['C', 'T'] else None
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        player.set_wage_offer()

class WaitForAllPlayers(WaitPage):
    wait_for_all_groups = True

class WageOffer(Page):
    form_model = 'player'
    form_fields = ['accepted']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'wage_offer': player.wage_offer
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        player.set_earnings()

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'reservation_wage': player.reservation_wage,
            'wage_offer': player.wage_offer,
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
        return player.round_number == Constants.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        player.set_total_earnings()
        return {
            'selected_round': player.in_round(random.randint(1, Constants.NUM_ROUNDS)),
            'total_earnings': player.total_earnings,
            'show_up_fee': Constants.SHOW_UP_FEE,
            'conversion_rate': Constants.EXCHANGE_RATE,
        }

page_sequence = [
    SetReservationWage,
    WaitForAllPlayers,  # Ensure all players wait here to synchronize
    WageOffer,
    Results,
    TeamResults,
    FinalEarnings
]
