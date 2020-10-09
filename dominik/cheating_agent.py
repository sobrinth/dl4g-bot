import logging
import numpy as np

from jass.agents.agent import Agent
from jass.game.game_state import GameState
from jass.game.rule_schieber import RuleSchieber
from jass.game.const import PUSH, MAX_TRUMP, card_values, card_strings


class CheatingAgent(Agent):

    def __init__(self, timeout=10):
        self.__logger = logging.getLogger(__name__)
        self.__rule = RuleSchieber()
        self.__rng = np.random.default_rng()

    def action_trump(self, state: GameState) -> int:
        """
        Select trump according to max trick-values
        """
        trump = 0
        max_sum_in_color = 0
        # max_number_in_color = 0 Count the amount of cards in a given color
        self.__logger.info('Requesting Trump')
        for c in range(MAX_TRUMP):
            sum_in_color = (state.hand * card_values[c]).sum()
            if sum_in_color > max_sum_in_color:
                max_sum_in_color = sum_in_color
                trump = c

        if state.forehand == -1:
            if max_sum_in_color < 55:
                return PUSH
        return trump

    def action_play_card(self, state: GameState) -> int:
        self.__logger.info('Card request')
        # cards are one hot encoded
        valid_cards = self.__rule.get_valid_cards_from_obs(state)
        # convert to list and draw a value
        card = -1
        value = 0
        for c in range(36):
            if valid_cards[c] != 0:
                new_val = 1 + card_values[state.trump][c]
                if new_val > value:
                    card = c
                    value = new_val
        if card == -1:
            card = self.__rng.choice(np.flatnonzero(valid_cards))
        self.__logger.info('Played card: {}'.format(card_strings[card]))
        return card

    def minimax_select(self, state: GameState) -> int:

        return 0
