import random
import time
from pathlib import Path

from rich.console import Group
from rich.live import Live
from rich.progress import Progress
import torch

import heuristics
from AI_player import AIPlayer
from AI_type import AI_type
from board import Board
from game import Game
from neural_network import *

BOARD_SIZE = 3


def progress_bar(x_wins, o_wins, draws, total, progress=None):
    text = (
        f"x wins: {x_wins / total * 100:05.2f}% ({x_wins})\n"
        f"o wins: {o_wins / total * 100:05.2f}% ({o_wins})\n"
        f"draws:  {draws / total * 100:05.2f}% ({draws})\n"
    )
    if progress is None:
        return text
    return Group(text, progress)


def play_games(player_x, player_o):
    player_x.token = 'x'
    player_o.token = 'o'

    x_wins = o_wins = draws = 0
    progress = Progress()
    with Live(
        progress_bar(x_wins, o_wins, draws, 1, progress),
        refresh_per_second=4,
    ) as live:
        for game_number in progress.track(range(1_000), description="Playing..."):
            board = Board(BOARD_SIZE)
            player_x.board = player_o.board = board
            game = Game(board, player_x, player_o, print_gameplay=False)

            game.play()

            if game.winner is None:
                draws += 1
            elif game.winner == 'x':
                x_wins += 1
            else:
                o_wins += 1

            live.update(progress_bar(x_wins, o_wins, draws, game_number + 1, progress))
        live.update(progress_bar(x_wins, o_wins, draws, game_number + 1))


nn = NeuralNetwork.from_state_dict(
    torch.load(Path(__file__).parent.parent / f"train_data/nn_random_{BOARD_SIZE}.tar")
)
board = Board(BOARD_SIZE)
with torch.no_grad():
    nn_player = AIPlayer(board, "o", AI_type.NEURAL_NETWORK, nn=nn)
    random_player = AIPlayer(board, "x", AI_type.RANDOM)
    print("Neural Network vs Random:")
    play_games(nn_player, random_player)
    print("Random vs Neural Network:")
    play_games(random_player, nn_player)
    minimax_player = AIPlayer(board, "o", AI_type.MINIMAX, 3, heuristics.extended_heuristic)
    print("Neural Network vs Minimax:")
    play_games(nn_player, minimax_player)
    print("Minimax vs Neural Network:")
    play_games(minimax_player, nn_player)
    alpha_beta_player = AIPlayer(board, "o", AI_type.ALPHA_BETA, 1, heuristics.extended_heuristic)
    print("Neural Network vs Alpha-beta:")
    play_games(nn_player, alpha_beta_player)
    print("Alpha-beta vs Neural Network:")
    play_games(alpha_beta_player, nn_player)
