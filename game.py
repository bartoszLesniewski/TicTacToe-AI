import time


class Game:
    def __init__(self, board, player1, player2, print_gameplay=True):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.winner = None
        self.print_gameplay = print_gameplay
        self.x_timings = []
        self.o_timings = []

    def play(self):
        while True:
            if self.print_gameplay:
                print("======= PLAYER 1: " + self.player1.token + " | PLAYER 2: " + self.player2.token + " =======")
                self.board.draw()

            start = time.monotonic()
            self.current_player.move()
            stop = time.monotonic()
            if self.current_player.token == 'x':
                self.x_timings.append(stop-start)
            else:
                self.o_timings.append(stop-start)

            result = self.board.check_for_end()
            if result[0]:
                self.winner = result[1]
                break

            self.switch_player()

        if self.print_gameplay:
            self.show_result()

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def show_result(self):
        self.board.draw()
        if self.winner is None:
            print("======= DRAW =======")
        else:
            print("======= WINNER: " + self.winner + " =======")
