class Game:
    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.winner = None

    def play(self):
        while True:
            print("======= PLAYER 1: " + self.player1.token + " | PLAYER 2: " + self.player2.token + " =======")

            self.board.draw()
            self.current_player.move()

            result = self.board.check_for_end()
            if result[0]:
                self.winner = result[1]
                break

            self.switch_player()

        self.show_result()

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def show_result(self):
        self.board.draw()
        if self.winner is None:
            print("======= DRAW =======")
        else:
            print("======= WINNER: " + self.winner + " =======")
