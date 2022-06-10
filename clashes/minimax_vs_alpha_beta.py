from AI_player import AIPlayer
from AI_type import AI_type
from board import Board
from game import Game

board = Board(3)
minimax_player = AIPlayer(board, "x", AI_type.MINIMAX, 1)
alpha_beta_player = AIPlayer(board, "o", AI_type.ALPHA_BETA, 4)

game = Game(board, minimax_player, alpha_beta_player)
game.play()
