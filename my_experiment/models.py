
from otree.api import *
import random


class C(BaseConstants):
    NAME_IN_URL = 'my_experiment'
    PLAYERS_PER_GROUP = None  # Individual task
    NUM_ROUNDS = 1
    # CTB Constants
    BUDGET = cu(100)
    INTEREST_RATES = [1, 1.05, 1.1, 1.15, 1.2]
    # Regret Task Constants
    INITIAL_ENDOWMENT = cu(150)
    LOTTERY_A = {"outcomes": [cu(100), cu(-50)], "probabilities": [0.5, 0.5]}
    LOTTERY_B = {"outcomes": [cu(200), cu(-100)], "probabilities": [0.3, 0.7]}


class Subsession(BaseSubsession):
    def creating_session(self):
        # Run only once, at the start of the experiment
        for p in self.get_players():
            # Randomly pick 'treatment' or 'control'
            p.treatment_group = random.choice(['treatment', 'control'])
        if self.round_number == 1:
            prolific = self.session.config.get("prolific-link", 60)  # default to 60 if not set
            # You can store `time` on the session or pass it to players
            self.session.vars["prolific-link"] = prolific  # optional storage


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Privacy policy fields

    outcome = models.CurrencyField()
    unchosen_outcome = models.CurrencyField(
        initial=None,
        doc="What the unchosen lottery would have paid out"
    )

    confirm_age = models.BooleanField(
        label="I am at least 18 years old and consent to participate",
    )
    confirm_withdraw = models.BooleanField(
        label="I understand I can withdraw without penalty (by closing the software)",
    )
    confirm_privacy = models.BooleanField(
        label="I have read the Privacy Notice",
    )
    treatment_group = models.StringField(
        choices=['treatment', 'control'],
        doc="Which experimental condition the participant is in",
    )

    # Regret Task Fields
    chosen_lottery = models.StringField()
    arrow_angle = models.FloatField(initial=0)
    arrow_speed = models.FloatField(initial=0)
    stopped_angle = models.FloatField()
    outcome = models.CurrencyField()

    # CTB Task Fields
    alloc_early1 = models.CurrencyField()
    alloc_late1 = models.CurrencyField()
    alloc_early2 = models.CurrencyField()
    alloc_late2 = models.CurrencyField()
    alloc_early3 = models.CurrencyField()
    alloc_late3 = models.CurrencyField()
    alloc_early4 = models.CurrencyField()
    alloc_late4 = models.CurrencyField()
    alloc_early5 = models.CurrencyField()
    alloc_late5 = models.CurrencyField()
    payoff_decision = models.IntegerField()
    payoff_now = models.CurrencyField()
    payoff_later = models.CurrencyField()

    # Questionnaire Fields
    q_regret_curiosity = models.IntegerField(choices=range(1, 6))
    q_regret_failure = models.IntegerField(choices=range(1, 6))
    q_assess_opportunities = models.IntegerField(choices=range(1, 6))
    q_high_standards = models.IntegerField(choices=range(1, 6))
    q_choice_difficulty = models.IntegerField(choices=range(1, 6))
    q_shopping_difficulty = models.IntegerField(choices=range(1, 6))
    q_future_thinking = models.IntegerField(choices=range(1, 6))
    q_sacrifice = models.IntegerField(choices=range(1, 6))
    q_immediate_concerns = models.IntegerField(choices=range(1, 6))
    q_regret_counterfactual = models.IntegerField(
        choices=range(1, 6),
        label="“Had I made a different choice, things would have turned out better for me”"
    )

    prolific_id = models.StringField(
        label="Please insert your Prolific ID:",
        blank=False,  # forces them to type something
    )

