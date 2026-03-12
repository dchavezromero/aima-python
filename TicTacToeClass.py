"""
TicTacToeClass.py
CS 534 - Individual Project Assignment 3

Description: This module imports the TicTacToe game class, search algorithms,
             and player functions from games4e.py. It adds the two player
             wrapper functions not already defined in games4e.py
             (minimax_player and heuristic_alpha_beta_player) and provides
             a player selection mapping used by TicTacToeGameApp.py.
"""

from games4e import (
    minmax_decision,
    alpha_beta_cutoff_search,
    random_player,
    alpha_beta_player,
    mcts_player,
    query_player
)


# --- Player wrappers not provided in games4e.py ---

def minimax_player(game, state):
    """A player that uses the Minimax decision algorithm."""
    return minmax_decision(state, game)


def heuristic_alpha_beta_player(game, state):
    """A player that uses Alpha-Beta search with cutoff (heuristic evaluation)."""
    return alpha_beta_cutoff_search(state, game)


# --- Player selection mapping ---

PLAYER_MAP = {
    1: ("Random Player", random_player),
    2: ("MiniMax Player", minimax_player),
    3: ("Alpha Beta Player", alpha_beta_player),
    4: ("Heuristic Alpha Beta Player", heuristic_alpha_beta_player),
    5: ("MCTS Player", mcts_player),
    6: ("Query Player", query_player)
}


def get_player(choice):
    """Return (name, function) tuple for the given player choice number.

    Args:
        choice (int): Player selection number (1-6).

    Returns:
        tuple or None: (player_name, player_function) if valid, else None.
    """
    return PLAYER_MAP.get(choice)