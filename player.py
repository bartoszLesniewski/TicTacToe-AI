class Player:
    def __init__(self, board, token):
        self.board = board
        self.token = token

    def move(self):
        while True:
            str_position = input("Enter the position on which you want to make a move: ")
            str_position = str_position.split()
            try:
                position = (int(str_position[0]), int(str_position[1]))
                if self.check_move(position):
                    break
                else:
                    print("Given position is already taken! Please try again.")
            except ValueError:
                print("Invalid input data! Please try again.")
            except IndexError:
                print("Given position is out of range! Please try again.")

        self.make_move(position)

    def check_move(self, position):
        return self.board.states[position[0]][position[1]] == "_"

    def make_move(self, position):
        self.board.states[position[0]][position[1]] = self.token