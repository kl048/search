import sys

from otree.api import *


class CRT(Page):
    solutions = {
        'quiz1': 5,
        'quiz2': 5,
        'quiz3': 47,
        'quiz4': 9,
        'quiz5': 12,
        'quiz6': 14,
        'quiz7': 1,
    }

c = cu
doc = 'Focal point'
class C(BaseConstants):
    NAME_IN_URL = 'CRT'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ECU_LABEL = 'ECUs'
    EXCHANGE_RATE_TWO_FIRMS = 0.00715

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    num_failed_attempts = models.IntegerField(initial=0)
    failed_too_many = models.BooleanField(initial=False)
    num_correct_answers = models.IntegerField(initial=0)
    payment_for_correct_answers = models.CurrencyField(initial=0)

    quiz1 = models.IntegerField(label='A bat and a ball cost $1.10 in total.  The bat costs $1.00 more than the ball.  How much does the ball cost (in cents)?')
    quiz1_wrong = models.IntegerField(initial=0)

    quiz2 = models.IntegerField(
        label='If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?')
    quiz2_wrong = models.IntegerField(initial=0)

    quiz3 = models.IntegerField(label='In a lake, there is a patch of lily pads.  Every day, the patch doubles in size.'
        'If it takes 48 days for the patch to cover the entire lake, how long would it take for the patch to cover half the lake?')
    quiz3_wrong = models.IntegerField(initial=0)

    quiz4 = models.IntegerField(label='A box of staples has a length of 6 cm, a width of 7 cm, and a volume of 378 cm cubed.  What is the height of the box?')
    quiz4_wrong = models.IntegerField(initial=0)

    quiz5 = models.IntegerField(label='A basketball player averaged 20 points a game over the course of six games. His scores in five of those games were 23, 18, 16, 24, and 27.'
        'How many points did he score in the sixth game?')
    quiz5_wrong = models.IntegerField(initial=0)

    quiz6 = models.IntegerField(label='A physical education class has three times as many girls as boys.  During a class basketball game,'
        'the girls average 18 points each, and the class as a whole averages 17 points per person.  How many points does each boy score on average?'
    )
    quiz6_wrong = models.IntegerField(initial=0)

    quiz7 = models.IntegerField(
        label='Please enter your label (the number assigned to you).'
    )
    quiz7_wrong = models.IntegerField(initial=0)


class crt(Page):
    form_model = 'player'
    form_fields = ['quiz7', 'quiz1', 'quiz2', 'quiz3', 'quiz4', 'quiz5', 'quiz6']

    @staticmethod
    def error_message(player: Player, values):
        # alternatively, you could make quiz1_error_message, quiz2_error_message, etc.
        # but if you have many similar fields, this is more efficient.
        solutions = dict(
            quiz1=(5,5),
            quiz2=(5,5),
            quiz3=(47,47),
            quiz4=(9,9),
            quiz5=(12,12),
            quiz6=(14,14),
            quiz7=(1,1),
        )

        # error_message can return a dict whose keys are field names and whose
        # values are error messages
        errors = {
            k: solutions[k][1] for k, v in values.items () if v != solutions[k][0]
        }


        for k in errors.keys():
            num = getattr(player, f'{k}_wrong')
            setattr(player, f'{k}_wrong', num + 1)

        # print('errors is', errors)
        if errors:
            player.num_failed_attempts += 1
            if player.num_failed_attempts >= 1:
                player.failed_too_many = True
                # we don't return any error here; just let the user proceed to the
                # next page, but the next page is the 'Next' page that takes them to a page with next button
            else:
                return errors



class next(Page):

        @staticmethod
        def is_displayed(player: Player):
            return player.round_number == C.NUM_ROUNDS

        @staticmethod
        def is_displayed(player: Player):
            return player.failed_too_many



page_sequence = [crt, next]