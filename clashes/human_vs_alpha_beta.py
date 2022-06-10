from AI_player import AIPlayer
from AI_type import AI_type
from board import Board
from game import Game
from player import Player

board = Board(3)
human_player = Player(board, "x")
ai_player = AIPlayer(board, "o", AI_type.ALPHA_BETA, 1)

game = Game(board, human_player, ai_player)
game.play()