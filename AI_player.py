import copy
import math
import random
from collections import deque

import torch

from AI_type import AI_type
from player import Player
from neural_network import InvalidGameState


class AIPlayer(Player):
    def __init__(self, board, token, ai_type, max_depth=None, heuristic=None, nn=None, training=False):
        super().__init__(board, token)
        self.ai_type = ai_type
        self.max_depth = max_depth
        self.heuristic = heuristic
        self.nn = nn
        self.training = training
        self.epsilon = None
        self.move_history = deque()

    @property
    def name(self):
        if self.heuristic is None:
            return self.ai_type.value
        return f"{self.ai_type.value} with {self.heuristic.__name__} heuristic"

    def move(self):
        move = None
        if self.ai_type == AI_type.RANDOM:
            possible_moves = self.board.get_possible_moves()
            move = random.choice(possible_moves)
        elif self.ai_type == AI_type.MINIMAX:
            move = self.minimax(self.board, self.max_depth)[1]
        elif self.ai_type == AI_type.ALPHA_BETA:
            move = self.alpha_beta(self.board, self.max_depth)[1]
        elif self.ai_type == AI_type.NEURAL_NETWORK:
            move = self.neural_network(self.board)

        self.make_move(move)

    def get_opponent_token(self):
        if self.token == "x":
            return "o"
        else:
            return "x"

    def minimax(self, board, depth=2, maximizingPlayer=True):
        result = board.check_for_end()
        if result[0]:
            if result[1] == self.token:
                return math.inf, None
            elif result[1] is None:
                return 0, None
            else:
                return -math.inf, None

        if depth == 0:
            return self.heuristic(board, self.token), None
            # return -1, None

        best_score = -math.inf if maximizingPlayer else math.inf
        best_move = None

        for move in board.get_possible_moves():
            new_board = copy.deepcopy(board)
            new_board.states[move[0]][move[1]] = (self.token if maximizingPlayer else self.get_opponent_token())
            score = self.minimax(new_board, depth-1, not maximizingPlayer)[0]

            if maximizingPlayer:
                if score > best_score or best_move is None:
                    best_score = score
                    best_move = move
            else:
                if score < best_score or best_move is None:
                    best_score = score
                    best_move = move

        return best_score, best_move

    def alpha_beta(self, board, depth=2, maximizingPlayer=True, alpha=-math.inf, beta=math.inf):
        result = board.check_for_end()
        if result[0]:
            if result[1] == self.token:
                return math.inf, None
            elif result[1] is None:
                return 0, None
            else:
                return -math.inf, None

        if depth == 0:
            return self.heuristic(board, self.token), None
            # return -1, None

        best_score = -math.inf if maximizingPlayer else math.inf
        best_move = None

        for move in board.get_possible_moves():
            new_board = copy.deepcopy(board)
            new_board.states[move[0]][move[1]] = "o" if maximizingPlayer else "x"
            score = self.alpha_beta(new_board, depth-1, not maximizingPlayer, alpha, beta)[0]

            if maximizingPlayer:
                if score > best_score or best_move is None:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
            else:
                if score < best_score or best_move is None:
                    best_score = score
                    best_move = move

                beta = min(beta, best_score)
                if alpha >= beta:
                    break

        return best_score, best_move

    def neural_network(self, board):
        if self.training:
            move_idx = self.choose_nn_move(board)
            self.move_history.appendleft((board, move_idx))
        else:
            move_idx = self.choose_valid_nn_move(board)

        move = (move_idx // board.size, move_idx % board.size)
        if self.training and move not in board.get_possible_moves():
            raise InvalidGameState

        return move

    def choose_nn_move(self, board):
        if self.epsilon > 0:
            if random.random() < self.epsilon:
                return random.randrange(board.size * board.size)

        with torch.no_grad():
            return torch.argmax(self.nn.policy_network(board.tensor)).item()

    def choose_valid_nn_move(self, board):
        q_values = self.nn.target_network(board.tensor)
        valid_q_values = [
            (x * board.size + y, q_values[x * board.size + y].item())
            for x, y in self.board.get_possible_moves()
        ]
        return max(valid_q_values, key=lambda tup: tup[1])[0]
