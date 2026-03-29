"""
TicTacToeClass.py

Description: This module imports the TicTacToe game class, search algorithms,
             and player functions from games4e.py. It adds the two player
             wrapper functions not already defined in games4e.py
             (minimax_player and heuristic_alpha_beta_player) and provides
             a player selection mapping used by TicTacToeGameApp.py.

Author: Dennis Chavez Romero
Course: CS 534 - Artificial Intelligence
Date: 03/29/2026
"""

from games4e import (
    TicTacToe,
    minmax_decision,
    alpha_beta_cutoff_search,
    random_player,
    alpha_beta_player,
    mcts_player,
    query_player
)


def minimax_player(game, state):
    """Select the best move using the Minimax decision algorithm.

    This is a wrapper around minmax_decision() from games4e.py that
    conforms to the player function signature: player_func(game, state) -> action.

    Args:
        game  (TicTacToe): The current game instance.
        state (GameState): The current board state.

    Returns:
        tuple: The (row, col) action chosen by full-depth Minimax search.
    """
    return minmax_decision(state, game)


def heuristic_alpha_beta_player(game, state):
    """Select the best move using Alpha-Beta search with a depth cutoff.

    This is a wrapper around alpha_beta_cutoff_search() from games4e.py
    that conforms to the player function signature: player_func(game, state) -> action.

    Args:
        game  (TicTacToe): The current game instance.
        state (GameState): The current board state.

    Returns:
        tuple: The (row, col) action chosen by heuristic Alpha-Beta search.
    """
    return alpha_beta_cutoff_search(state, game)

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