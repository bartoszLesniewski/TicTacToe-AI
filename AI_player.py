import copy
import math
import random

from heuristics import heuristic_function
from human_player import Player


class AIPlayer(Player):
    def __init__(self, board, token, level):
        super().__init__(board, token)
        self.level = level

    def move(self):
        if self.level == "EASY":
            possible_moves = self.board.get_possible_moves()
            random_move = random.choice(possible_moves)
            self.make_move(random_move)
        else:
            move = self.minimax(self.board, 1, True)[1]
            self.make_move(move)

    def minimax(self, board, depth=2, maximizingPlayer=True): #, alpha=-math.inf, beta=math.inf):
        result = board.check_for_end()
        if result[0]:
            if result[1] == self.token:
                return math.inf, None
            elif result[1] is None:
                return 0, None
            else:
                return -math.inf, None

        if depth == 0:
            return heuristic_function(board, self.token), None
            # return -1, None

        best_score = -math.inf if maximizingPlayer else math.inf
        best_move = None

        for move in board.get_possible_moves():
            new_board = copy.deepcopy(board)
            new_board.states[move[0]][move[1]] = "o" if maximizingPlayer else "x"
            score = self.minimax(new_board, depth-1, not maximizingPlayer)[0] #, alpha, beta)[0]

            if maximizingPlayer:
                if score > best_score:
                    best_score = score
                    best_move = move
                #alpha = max(alpha, best_score)
                #if alpha >= beta:
                #    break
            else:
                if score < best_score:
                    best_score = score
                    best_move = move

                #beta = min(beta, best_score)
                #if alpha >= beta:
                #    break

        return best_score, best_move
