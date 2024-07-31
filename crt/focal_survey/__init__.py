from otree.api import *

c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='What is your age?', max=125, min=13)
    gender = models.StringField(choices=[['Male', 'Male'], ['Female', 'Female'], ['Non-binary', 'Non-binary'],
                                         ['Prefer not to say', 'Prefer not to say']], label='What is your gender?',
                                widget=widgets.RadioSelect)
    major = models.StringField(
        choices=[['Agriculture, Food and Life Sciences', 'Agriculture, Food and Life Sciences'], ['Architecture and Design', 'Architecture and Design'],
                 ['Arts and Sciences', 'Arts and Sciences'],
                 ['Business', 'Business'], ['Education and Health', 'Education and Health'], ['Engineering', 'Engineering'],
                 ['Law', 'Law'], ['Others', 'Others']],
        label='Which of the following best describes your major of study?', widget=widgets.RadioSelect)
    econ = models.IntegerField(label='How many Economics classes have you taken so far? (must specify a number)',
                               max=32, min=0)
    uni = models.IntegerField(
        label='How many years of university study have you completed (enter 0 if in first year)? (must specify a number)',
        max=10, min=0)
    gpa = models.FloatField(label='What is your university GPA? (must specify a number)', max=7, min=0)
    risk_preference = models.IntegerField(
        choices=[[0, '0'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'], [8, '8'], [9, '9'], [10, '10']],
        label='Please tell us, in general, how willing or unwilling you are to take risks. Please use a scale from 0 to 10, where 0 means you are "completely unwilling to take risks" and a 10 means you are "very willing to take risks". You can also use any numbers between 0 and 10 to indicate where you fall on the scale, like 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.',
        widget=widgets.RadioSelect)
    time_discounting = models.IntegerField(
        choices=[[0, '0'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'], [8, '8'], [9, '9'],
                 [10, '10']],
        label='In comparison to others, are you a person who is generally willing to give up something today in order to benefit from that in the future or are you not willing to do so? Please use a scale from 0 to 10, where a 0 means, “you are completely unwilling to give up something today" and a 10 means “you are very willing to give up something today". You can also use the values in-between to indicate where you fall on the scale.',
        widget=widgets.RadioSelect)
    trust = models.IntegerField(
        choices=[[0, '0'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'], [8, '8'], [9, '9'],
                 [10, '10']],
        label='How well does the following statement describe you as a person? As long as I am not convinced otherwise, I assume that people have only the best intentions. Please use a scale from 0 to 10, where 0 means “does not describe me at all" and a 10 means “describes me perfectly". You can also use the values in-between to indicate where you fall on the scale.',
        widget=widgets.RadioSelect)
    positive_reciprocity = models.IntegerField(
        choices=[[5, '5'], [10, '10'], [15, '15'], [20, '20'], [25, '25'], [30, '30']],
        label='Imagine the following situation: you are shopping in an unfamiliar city and realize you lost your way. You ask a stranger for directions. The stranger offers to take you with their car to your destination. The ride takes about 20 minutes and costs the stranger about 20 Dollars in total. The stranger does not want money for it. You carry six bottles of wine with you. The cheapest bottle costs 5 Dollars, the most expensive one 30 Dollars. You decide to give one of the bottles to the stranger as a thank-you gift. Which bottle do you give? Respondents can choose from the following options: The bottle for 5, 10, 15, 20, 25, or 30 Dollars)',
        widget=widgets.RadioSelect)
    negative_reciprocity = models.IntegerField(
        choices=[[0, '0'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'], [8, '8'], [9, '9'],
                 [10, '10']],
        label='How do you see yourself: Are you a person who is generally willing to punish unfair behavior even if this is costly? Please use a scale from 0 to 10, where 0 means you are “not willing at all to incur costs to punish unfair behavior" and a 10 means you are “very willing to incur costs to punish unfair behavior". You can also use the values in-between to indicate where you fall on the scale.',
        widget=widgets.RadioSelect)
    Extraverted_enthusiastic = models.StringField(
        choices= [['Disagree strongly', 'Disagree strongly'], ['Disagree moderately', 'Disagree moderately'],
                  ['Disagree a little', 'Disagree a little'], ['Neither agree nor disagree', 'Neither agree nor disagree'],
                  ['Agree a little', 'Agree a little'], ['Agree moderately', 'Agree moderately'],
                  ['Agree strongly', 'Agree strongly']],
        label = 'I see myself as: Extraverted, enthusiastic.', widget = widgets.RadioSelect)
    Critical_quarrelsome = models.StringField(
        choices=[['Disagree strongly', 'Disagree strongly'], ['Disagree moderately', 'Disagree moderately'],
                 ['Disagree a little', 'Disagree a little'],
                 ['Neither agree nor disagree', 'Neither agree nor disagree'],
                 ['Agree a little', 'Agree a little'], ['Agree moderately', 'Agree moderately'],
                 ['Agree strongly', 'Agree strongly']],
        label='I see myself as: Critical, quarrelsome.', widget=widgets.RadioSelect)
    Dependable_self_disciplined = models.StringField(
        choices=[['Disagree strongly', 'Disagree strongly'], ['Disagree moderately', 'Disagree moderately'],
                 ['Disagree a little', 'Disagree a little'],
                 ['Neither agree nor disagree', 'Neither agree nor disagree'],
                 ['Agree a little', 'Agree a little'], ['Agree moderately', 'Agree moderately'],
                 ['Agree strongly', 'Agree strongly']],
        label='I see myself as: Dependable, self-disciplined.', widget=widgets.RadioSelect)
    Anxious_easily_upset = models.StringField(
        choices=[['Disagree strongly', 'Disagree strongly'], ['Disagree moderately', 'Disagree moderately'],
                 ['Disagree a little', 'Disagree a little'],
                 ['Neither agree nor disagree', 'Neither agree nor disagree'],
                 ['Agree a little', 'Agree a little'], ['Agree moderately', 'Agree moderately'],
                 ['Agree strongly', 'Agree strongly']],
        label='I see myself as: Anxious, easily upset.', widget=widgets.RadioSelect)
    Open_to_new_experiences_complex = models.StringField(
        choices=[['Disagree strongly', 'Disagree strongly'], ['Disagree moderately', 'Disagree moderately'],
                 ['Disagree a little', 'Disagree a little'],
                 ['Neither agree nor disagree', 'Neither agree nor disagree'],
                 ['Agree a little', 'Agree a little'], ['Agree moderately', 'Agree moderately'],
                 ['Agree strongly', 'Agree strongly']],
        label='I see myself as: Open to new experiences, complex.', widget=widgets.RadioSelect)
    Reserved_quiet = models.StringField(
        choices=[['Disagree strongly', 'Disagree strongly'], ['Disagree moderately', 'Disagree moderately'],
                 ['Disagree a little', 'Disagree a little'],
                 ['Neither agree nor disagree', 'Neither agree nor disagree'],
                 ['Agree a little', 'Agree a little'], ['Agree moderately', 'Agree moderately'],
                 ['Agree strongly', 'Agree strongly']],
        label='I see myself as: Reserved, quiet.', widget=widgets.RadioSelect)
    Sympathetic_warm = models.StringField(
        choices=[['Disagree strongly', 'Disagree strongly'], ['Disagree moderately', 'Disagree moderately'],
                 ['Disagree a little', 'Disagree a little'],
                 ['Neither agree nor disagree', 'Neither agree nor disagree'],
                 ['Agree a little', 'Agree a little'], ['Agree moderately', 'Agree moderately'],
                 ['Agree strongly', 'Agree strongly']],
        label='I see myself as: Sympathetic, warm.', widget=widgets.RadioSelect)
    Disorganized_careless = models.StringField(
        choices=[['Disagree strongly', 'Disagree strongly'], ['Disagree moderately', 'Disagree moderately'],
                 ['Disagree a little', 'Disagree a little'],
                 ['Neither agree nor disagree', 'Neither agree nor disagree'],
                 ['Agree a little', 'Agree a little'], ['Agree moderately', 'Agree moderately'],
                 ['Agree strongly', 'Agree strongly']],
        label='I see myself as: Disorganized, careless.', widget=widgets.RadioSelect)
    Calm_emotionally_stable = models.StringField(
        choices=[['Disagree strongly', 'Disagree strongly'], ['Disagree moderately', 'Disagree moderately'],
                 ['Disagree a little', 'Disagree a little'],
                 ['Neither agree nor disagree', 'Neither agree nor disagree'],
                 ['Agree a little', 'Agree a little'], ['Agree moderately', 'Agree moderately'],
                 ['Agree strongly', 'Agree strongly']],
        label='I see myself as: Calm, emotionally stable.', widget=widgets.RadioSelect)
    Conventional_uncreative = models.StringField(
        choices=[['Disagree strongly', 'Disagree strongly'], ['Disagree moderately', 'Disagree moderately'],
                 ['Disagree a little', 'Disagree a little'],
                 ['Neither agree nor disagree', 'Neither agree nor disagree'],
                 ['Agree a little', 'Agree a little'], ['Agree moderately', 'Agree moderately'],
                 ['Agree strongly', 'Agree strongly']],
        label='I see myself as: Conventional, uncreative.', widget=widgets.RadioSelect)
    reasoning = models.LongStringField(
        label='How did you make your price decisions today? Please explain in a few lines.'
    )


class demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'major', 'econ', 'uni', 'gpa']


class tipi(Page):
    form_model = 'player'
    form_fields = ['Extraverted_enthusiastic','Critical_quarrelsome','Dependable_self_disciplined','Anxious_easily_upset',
                   'Open_to_new_experiences_complex','Reserved_quiet','Sympathetic_warm','Disorganized_careless',
                   'Calm_emotionally_stable','Conventional_uncreative']


class behavioral(Page):
    form_model = 'player'
    form_fields = ['reasoning', 'risk_preference', 'time_discounting', 'trust', 'positive_reciprocity', 'negative_reciprocity']


class thankyou(Page):
    pass


page_sequence = [demographics, tipi, behavioral, thankyou]
