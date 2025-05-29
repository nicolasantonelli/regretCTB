import random
from otree.api import Page, cu
from .models import C


# ==============================================================================
# Regret Elicitation Task
# ==============================================================================

class PrivacyPolicy(Page):
    form_model = 'player'
    form_fields = ['confirm_age', 'confirm_withdraw', 'confirm_privacy']


class Instructions(Page):
    pass


class ProlificPage(Page):
    form_model = 'player'
    form_fields = ['prolific_id']


class InstructionsRegret(Page):
    pass


class RegretTask(Page):
    form_model = 'player'
    form_fields = ['chosen_lottery']

    def vars_for_template(self):
        return {
            'prob_a': C.LOTTERY_A['probabilities'],
            'prob_b': C.LOTTERY_B['probabilities'],
        }

    def before_next_page(self, timeout_happened=False):
        # Randomize arrow parameters
        self.player.arrow_angle = random.uniform(0, 360)
        self.player.arrow_speed = random.uniform(15, 25)
        # todo: random player treatment (posso decidere la percentuale di control e di treatment)


class SpinArrow(Page):
    form_model = 'player'
    form_fields = ['stopped_angle']

    def vars_for_template(self):
        if self.player.chosen_lottery == 'A':
            chosen = C.LOTTERY_A
            unchosen = C.LOTTERY_B
        else:
            chosen = C.LOTTERY_B
            unchosen = C.LOTTERY_A
        return {
            'initial_angle': self.player.arrow_angle,
            'initial_speed': self.player.arrow_speed,
            'lottery': chosen,
            'treatment': self.player.treatment_group,
            'chosen_probs': chosen['probabilities'],
            'unchosen_probs': unchosen['probabilities'],
        }

    def before_next_page(self, timeout_happened=False):
        p = self.player
        spin_angle = p.stopped_angle % 360  # Renamed from 'angle' to 'spin_angle'

        def get_outcome(test_angle, probs, outcomes):
            """
            Given a clockwise angle (0-360), probabilities (summing to 1), and outcomes [win, loss],
            return the correct outcome.
            The first outcome corresponds to the first slice drawn starting at 90° (Math.PI/2).
            """
            start_angle = 90  # Drawing starts at 90°
            for prob, outcome in zip(probs, outcomes):
                slice_size = prob * 360
                end_angle = (start_angle + slice_size) % 360
                # handle wrapping across 360
                if start_angle < end_angle:
                    if start_angle <= test_angle < end_angle:
                        return outcome
                else:
                    if test_angle >= start_angle or test_angle < end_angle:
                        return outcome
                start_angle = end_angle
            return outcomes[-1]  # fallback

        if p.chosen_lottery == 'A':
            chosen = C.LOTTERY_A
            unchosen = C.LOTTERY_B
        else:
            chosen = C.LOTTERY_B
            unchosen = C.LOTTERY_A

        p.outcome = get_outcome(spin_angle, chosen['probabilities'], chosen['outcomes'])
        p.unchosen_outcome = get_outcome(spin_angle, unchosen['probabilities'], unchosen['outcomes'])
        p.participant.endowment = C.INITIAL_ENDOWMENT + p.outcome


class RegretPayoff(Page):
    def vars_for_template(self):
        p = self.player
        initial = C.INITIAL_ENDOWMENT   # from your constants
        gained = p.outcome             # the lottery result stored earlier
        final = initial + gained

        # Pre‑format as strings so templates need no filters
        gained_str = f"{gained:.0f}"
        final_str = f"{final:.0f}"
        unchosen_str = f"{p.unchosen_outcome:.0f}"
        unchosen_gain = p.unchosen_outcome
        unchosen_total = initial + unchosen_gain

        return {
            'initial': initial,
            'gained_str': gained_str,
            'unchosen_str': unchosen_str,
            'final_str': final_str,
            'is_treatment': p.treatment_group == 'treatment',
            'unchosen_total_str': f"{unchosen_total:.0f}",
        }
# ==============================================================================
# Convex Time Budget Task
# ==============================================================================


class InstructionsCTB(Page):
    pass


class CTB(Page):
    form_model = 'player'
    form_fields = [
        'alloc_early1', 'alloc_late1',
        'alloc_early2', 'alloc_late2',
        'alloc_early3', 'alloc_late3',
        'alloc_early4', 'alloc_late4',
        'alloc_early5', 'alloc_late5',
    ]

    def vars_for_template(self):
        # Use a fixed budget of 100 for everyone
        return {
            'budget': C.BUDGET,
            'rate_pairs': [
                (r, f"{r:.2f}") for r in C.INTEREST_RATES
            ],
        }

    def error_message(self, values):
        budget = float(C.BUDGET)
        for i in range(1, 6):
            early = float(values[f'alloc_early{i}'])
            late = float(values[f'alloc_late{i}'])
            if abs((early + late) - budget) > 0.01:
                return f"Decision {i} violates the budget constraint."

    def before_next_page(self, timeout_happened=False):
        # Randomly choose which decision is paid out
        self.player.payoff_decision = random.randint(1, 5)


class Payoff(Page):
    def vars_for_template(self):
        selected = random.randint(1, 5)
        p = self.player
        p.payoff_decision = selected

        early = getattr(p, f'alloc_early{selected}')
        late = getattr(p, f'alloc_late{selected}')
        rate = C.INTEREST_RATES[selected - 1]

        p.payoff_now = early
        p.payoff_later = cu(float(late) * rate)

        return {
            'endowment': p.participant.endowment,
            'payoff_now': p.payoff_now,
            'payoff_later': p.payoff_later,
        }


class AfterCTB(Page):
    pass


class Questionnaire(Page):
    form_model = 'player'
    form_fields = [
        'q_regret_curiosity',
        'q_regret_failure',
        'q_assess_opportunities',
        'q_high_standards',
        'q_choice_difficulty',
        'q_shopping_difficulty',
        'q_future_thinking',
        'q_sacrifice',
        'q_immediate_concerns',
        'q_regret_counterfactual',
    ]


class End(Page):
    def vars_for_template(self, timeout_happened=False):
        p = self.player
        # Which decision was randomly selected?
        selected = p.payoff_decision

        # Retrieve allocations
        early = getattr(p, f'alloc_early{selected}')
        late = getattr(p, f'alloc_late{selected}')
        rate = C.INTEREST_RATES[selected - 1]

        # Compute payoffs
        payoff_today = early
        payoff_future = cu(float(late) * rate)

        # Pre-format as strings (no decimals for tokens)
        today_str = f"{payoff_today:.2f}"
        future_str = f"{payoff_future:.2f}"

        return {
            'selected': selected,
            'today_str': today_str,
            'future_str': future_str,
        }

    def before_next_page(self, timeout_happened=False):
        # Randomly choose which of the 5 decisions is paid
        self.player.payoff_decision = random.randint(1, 5)


page_sequence = [PrivacyPolicy, ProlificPage, Instructions, InstructionsRegret,
                 RegretTask, SpinArrow, RegretPayoff, InstructionsCTB, CTB, AfterCTB, Questionnaire, End]
