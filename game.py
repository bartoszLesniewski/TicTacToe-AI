from AI_player import AIPlayer
from board import Board
from player import Player


class Game:
    def __init__(self):
        self.board = Board(3)
        self.player = Player(self.board, "x")
        self.ai_player = AIPlayer(self.board, "o", "MEDIUM")
        self.current_player = self.player
        self.winner = None

    def play(self):
        while True:
            print("======= YOU: " + self.player.token + " | AI Player: " + self.ai_player.token + " =======")
            print("AI Player's move..." if self.current_player == self.ai_player else "Your move...")
            self.board.draw()
            self.current_player.move()

            result = self.board.check_for_end()
            if result[0]:
                self.winner = result[1]
                break

            self.switch_player()

        self.show_result()

    def switch_player(self):
        self.current_player = self.ai_player if self.current_player == self.player else self.player

    def show_result(self):
        self.board.draw()
        if self.winner is None:
            print("======= DRAW =======")
        else:
            print("======= WINNER: " + self.winner + " =======")
