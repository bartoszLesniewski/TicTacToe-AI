import random
import time
from pathlib import Path

from rich.progress import track
import torch

import heuristics
from AI_player import AIPlayer
from AI_type import AI_type
from board import Board
from game import Game
from neural_network import *

GAME_COUNT = 10_000
BOARD_SIZE = 3


# allow reproducing results
seed = time.time_ns()
random.seed(seed)
print(f"Random seed: {seed}")

board = Board(BOARD_SIZE)
board.states = [
    ["x", "o", "o"],
    ["_", "x", "x"],
    ["_", "_", "o"],
]
nn = NeuralNetwork(BOARD_SIZE, seed)
with torch.no_grad():
    q_values = nn.target_network(board.tensor)

nn_player = AIPlayer(board, "x", AI_type.NEURAL_NETWORK, nn=nn, training=True)
random_player = AIPlayer(board, "o", AI_type.RANDOM)

def train():
    nn_player.epsilon = 0.7
    for game_number in track(
        range(GAME_COUNT), description=f"Training as player {nn_player.token}..."
    ):
        board = Board(BOARD_SIZE)
        nn_player.move_history.clear()
        random_player.board = nn_player.board = board

        game = Game(board, random_player, nn_player, print_gameplay=False)
        try:
            game.play()
        except InvalidGameState:
            reward = LOSS_REWARD
        else:
            if game.winner is None:
                reward = DRAW_REWARD
            elif game.winner == nn_player.token:
                reward = WIN_REWARD
            else:
                reward = LOSS_REWARD

        it = iter(nn_player.move_history)
        next_board, move_idx = next(it)

        backpropagate(nn, next_board, move_idx, reward)

        for board, move_idx in it:
            with torch.no_grad():
                qv = torch.max(nn.target_network(board.tensor)).item()

            # discount factor is 1.0 here so target value is just `qv`
            backpropagate(nn, board, move_idx, qv)

            next_board = board

        nn.update_target_network()

        # Lower epsilon after every 10% of the total game count
        if (game_number + 1) % (GAME_COUNT // 10) == 0:
            nn_player.epsilon = max(0, nn_player.epsilon - 0.1)
            print(f"{game_number + 1}/{GAME_COUNT} games, using epsilon={nn_player.epsilon}")


train()
nn_player.token = "o"
random_player.token = "x"
train()

torch.save(
    nn.state_dict(),
    Path(__file__).parent.parent / f"train_data/nn_random_{BOARD_SIZE}.tar",
)
