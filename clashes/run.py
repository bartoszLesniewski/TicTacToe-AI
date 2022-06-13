import itertools
import math
import random
import time
from pathlib import Path

from rich.console import Group
from rich.live import Live
from rich.progress import MofNCompleteColumn, Progress
import torch

from AI_player import AIPlayer
from AI_type import AI_type
from board import Board
from game import Game
from heuristics import *
from neural_network import *

BOARD_SIZE = 3


class Runner:
    SCALES = [(1.0, "sec"), (1e-3, "msec"), (1e-6, "usec"), (1e-9, "nsec")]

    def __init__(self, player_x, player_o, global_progress, *, game_count=1000):
        self.player_x = player_x
        self.player_o = player_o
        self.game_count = game_count
        self.global_progress = global_progress
        self.clear()

    def clear(self):
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        self.total = 0
        self.x_timings = []
        self.o_timings = []
        self.progress = Progress()

    @classmethod
    def format_time(cls, dt):
        for scale, unit in cls.SCALES:
            if dt >= scale:
                break

        return f"{dt / scale:.3g} {unit}"

    @staticmethod
    def get_mean_and_stdev(timings):
        mean = math.fsum(timings) / len(timings)
        return mean, (math.fsum([(x - mean) ** 2 for x in timings]) / len(timings)) ** 0.5

    def get_average_string(self, timings):
        mean, std = self.get_mean_and_stdev(timings)
        return (
            f"{self.format_time(mean)} +- {self.format_time(std)} per game"
            f" (mean +- std. dev. of {self.game_count} games)"
        )

    def get_count_string(self, count):
        if not self.total:
            return f"---.--% (0)"
        formatted = f"{count / self.total * 100:.2f}".rjust(6)
        return f"{formatted}% ({count})"

    def progress_bar(self, *, show_progress=True):
        text = (
            f"x wins: {self.get_count_string(self.x_wins)}\n"
            f"o wins: {self.get_count_string(self.o_wins)}\n"
            f"draws:  {self.get_count_string(self.draws)}\n"
        )
        if show_progress:
            return Group(text, self.progress, self.global_progress)
        text += f"x timings: {self.get_average_string(self.x_timings)}\n"
        text += f"o timings: {self.get_average_string(self.o_timings)}\n"
        return text

    def play_games(self):
        self.player_x.token = 'x'
        self.player_o.token = 'o'
        self.clear()

        print(f"{self.player_x.name} VS. {self.player_o.name}")

        with Live(self.progress_bar(), refresh_per_second=4) as live:
            for self.total in self.progress.track(
                range(1, self.game_count + 1), description="Playing..."
            ):
                board = Board(BOARD_SIZE)
                self.player_x.board = self.player_o.board = board
                game = Game(board, self.player_x, self.player_o, print_gameplay=False)

                game.play()
                self.x_timings.append(sum(game.x_timings))
                self.o_timings.append(sum(game.o_timings))

                if game.winner is None:
                    self.draws += 1
                elif game.winner == 'x':
                    self.x_wins += 1
                else:
                    self.o_wins += 1

                live.update(self.progress_bar())
            live.update(self.progress_bar(show_progress=False))


nn = NeuralNetwork.from_state_dict(
    torch.load(Path(__file__).parent.parent / f"train_data/nn_random_{BOARD_SIZE}.tar")
)
board = Board(BOARD_SIZE)
with torch.no_grad():
    functions = [simple_heuristic, extended_heuristic, advanced_heuristic]
    players = [
        AIPlayer(board, "o", AI_type.NEURAL_NETWORK, nn=nn),
        AIPlayer(board, "o", AI_type.RANDOM),
        *(AIPlayer(board, "o", AI_type.MINIMAX, 3, func) for func in functions),
        *(AIPlayer(board, "o", AI_type.ALPHA_BETA, 1, func) for func in functions),
    ]
    global_progress = Progress(*Progress.get_default_columns(), MofNCompleteColumn())
    for x_player, o_player in global_progress.track(
        list(itertools.permutations(players, 2)),
        description="Total".ljust(10),
    ):
        runner = Runner(x_player, o_player, global_progress)
        runner.play_games()
