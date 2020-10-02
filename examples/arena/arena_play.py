# HSLU
#
# Created by Thomas Koller on 7/28/2020
#

import logging
import numpy as np

from local_jass.agents.agent import Agent
from local_jass.arena.arena import Arena
from local_jass.agents.agent_random_schieber import AgentRandomSchieber
from local_jass.game.const import color_masks, card_strings
from local_jass.game.game_observation import GameObservation
from local_jass.game.rule_schieber import RuleSchieber
from jass4fun.jass4fun_agent import Jass4FunAgent


class MyAgent(Agent):
    """
    Sample implementation of a player to play Jass.
    """
    def __init__(self):
        # log actions
        self._logger = logging.getLogger(__name__)
        # Use rule object to determine valid actions
        self._rule = RuleSchieber()
        # init random number generator
        self._rng = np.random.default_rng()

    def action_trump(self, obs: GameObservation) -> int:
        trump = 0
        max_number_in_color = 0
        for c in range(4):
            number_in_color = (obs.hand * color_masks[c]).sum()
            if number_in_color > max_number_in_color:
                max_number_in_color = number_in_color
                trump = c
        return trump

    def action_play_card(self, obs: GameObservation) -> int:
        # cards are one hot encoded
        valid_cards = self._rule.get_valid_cards_from_obs(obs)
        # convert to list and draw a value
        card = self._rng.choice(np.flatnonzero(valid_cards))
        self._logger.debug('Played card: {}'.format(card_strings[card]))
        return card


def main():
    # Set the global logging level (Set to debug or info to see more messages)
    logging.basicConfig(level=logging.WARN)

    # setup the arena
    arena = Arena(nr_games_to_play=1000, save_filename='arena_games')
    player = MyAgent()
    my_player = Jass4FunAgent()

    arena.set_players(my_player, player, my_player, player)
    print('Playing {} games'.format(arena.nr_games_to_play))
    arena.play_all_games()
    print('Average Points Team 0: {:.2f})'.format(arena.points_team_0.mean()))
    print('Average Points Team 1: {:.2f})'.format(arena.points_team_1.mean()))


if __name__ == '__main__':
    main()
