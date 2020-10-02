import logging
import numpy as np

from local_jass.agents.agent import Agent
from local_jass.game.game_observation import GameObservation
from local_jass.game.rule_schieber import RuleSchieber
from local_jass.game.const import PUSH, MAX_TRUMP, card_values, card_strings


class Jass4FunAgent(Agent):

    def __init__(self, timeout=10):
        self._logger = logging.getLogger(__name__)
        self._rule = RuleSchieber()
        self._rng = np.random.default_rng()

    def action_trump(self, obs: GameObservation) -> int:
        """
        Select trump according to max trick-values
        """
        trump = 0
        max_sum_in_color = 0
        # max_number_in_color = 0 Count the amount of cards in a given color
        self._logger.info('Requesting Trump')
        for c in range(MAX_TRUMP):
            sum_in_color = (obs.hand * card_values[c]).sum()
            if sum_in_color > max_sum_in_color:
                max_sum_in_color = sum_in_color
                trump = c

        if obs.forehand == -1:
            if max_sum_in_color < 55:
                return PUSH
        return trump

    def action_play_card(self, obs: GameObservation) -> int:
        self._logger.info('Card request')
        # cards are one hot encoded
        valid_cards = self._rule.get_valid_cards_from_obs(obs)
        # convert to list and draw a value
        card = -1
        value = 0
        for c in range(36):
            if valid_cards[c] != 0:
                new_val = 1 + card_values[obs.trump][c]
                if new_val > value:
                    card = c
                    value = new_val
        if card == -1:
            card = self._rng.choice(np.flatnonzero(valid_cards))
        self._logger.info('Played card: {}'.format(card_strings[card]))
        return card
