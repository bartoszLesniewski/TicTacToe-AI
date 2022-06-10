from AI_player import AIPlayer
from board import Board
from game import Game
from human_player import Player

board = Board(3)
player1 = Player(board, "x")
player2 = AIPlayer(board, "o", "MEDIUM")

game = Game(board, player1, player2)
game.play()
