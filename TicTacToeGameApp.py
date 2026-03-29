"""
TicTacToeGameApp.py

Description: Main application that allows the human user to select two players
             from six available strategies and play a best-of-three Tic-Tac-Toe
             game. The game repeats upon user request.

Author: Dennis Chavez Romero
Course: CS 534 - Artificial Intelligence
Date: 03/29/2026
"""

from TicTacToeClass import TicTacToe, get_player


def select_player(prompt):
    """Prompt the user to select a valid player (1-6).
    Keeps asking until a valid selection is made.

    Args:
        prompt (str): The initial input prompt message.

    Returns:
        int: A valid player choice between 1 and 6.
    """
    choice_str = input(prompt)
    while True:
        try:
            choice = int(choice_str)
            if 1 <= choice <= 6:
                return choice
        except ValueError:
            pass
        choice_str = input("Could not find your player, please try again: ")


def play_round(game, player_x_func, player_o_func, round_num):
    """Play one round of TicTacToe.

    Args:
        game (TicTacToe): The TicTacToe game object.
        player_x_func: Player X's strategy function (callable(game, state)).
        player_o_func: Player O's strategy function (callable(game, state)).
        round_num (int): The current round number (1, 2, or 3).

    Returns:
        str or None: 'X' if Player X wins, 'O' if Player O wins, None for draw.
    """
    print(f"Round {round_num}:")
    state = game.initial

    while not game.terminal_test(state):
        player = state.to_move

        if player == 'X':
            print("Available Action by the Player X:", game.actions(state))
            action = player_x_func(game, state)
            print("The Action by the Player X Is", action)
            state = game.result(state, action)
            game.display(state)
            print()
            utility = game.compute_utility(state.board, action, player)
            print(f"Player X's Utility: {utility}")

            if game.terminal_test(state):
                if state.utility == 1:
                    print(f"Player X won the game in Round {round_num}")
                elif state.utility == 0 and len(state.moves) == 0:
                    print(f"Player X and Player O drew the game in Round {round_num}.")
                break
            print()
        else:
            action = player_o_func(game, state)
            state = game.result(state, action)
            game.display(state)
            print()
            utility = game.utility(state, player)
            print(f"Player O's Utility: {utility}")

            if game.terminal_test(state):
                if state.utility == -1:
                    print(f"Player O won the game in Round {round_num}")
                elif state.utility == 0 and len(state.moves) == 0:
                    print(f"Player X and Player O drew the game in Round {round_num}.")
                break
            print()

    if state.utility == 1:
        return 'X'
    elif state.utility == -1:
        return 'O'
    else:
        return None


def main():
    """Main function to run the Tic-Tac-Toe Game Application."""
    while True:
        print("Player Selection:")
        print("1. Random Player")
        print("2. MiniMax Player")
        print("3. Alpha Beta Player")
        print("4. Heuristic Alpha Beta Player")
        print("5. MCTS Player")
        print("6. Query Player")
        print()

        player_x_choice = select_player("Please enter your first player: ")
        player_o_choice = select_player("Please enter your second player: ")

        game = TicTacToe()
        _, player_x_func = get_player(player_x_choice)
        _, player_o_func = get_player(player_o_choice)

        wins_x = 0
        wins_o = 0

        for round_num in range(1, 4):
            print()
            winner = play_round(game, player_x_func, player_o_func, round_num)

            if winner == 'X':
                wins_x += 1
            elif winner == 'O':
                wins_o += 1

            # Case 1: A player won the first two rounds in a row
            if round_num == 2:
                if wins_x == 2:
                    print()
                    print("Player X can win two out of three rounds in the game.")
                    print("Player X is the winner.")
                    break
                elif wins_o == 2:
                    print()
                    print("Player O can win two out of three rounds in the game.")
                    print("Player O is the winner.")
                    break

            # After round 3, determine overall result
            if round_num == 3:
                if wins_x >= 2:
                    print()
                    print("Player X can win two out of three rounds in the game.")
                    print("Player X is the winner.")
                elif wins_o >= 2:
                    print()
                    print("Player O can win two out of three rounds in the game.")
                    print("Player O is the winner.")
                else:
                    print()
                    print("No Player can win two out of three rounds in the game.")
                    print("The game was a draw.")

        print()
        play_again = input("Would you like to play the game again? ")
        if play_again.strip().lower() not in ['yes', 'y']:
            print("Thank You for Playing Our Game!")
            break
        print()


if __name__ == "__main__":
    main()