class Board:
    def __init__(self, size):
        self.size = size
        self.states = [["_" for _ in range(size)] for _ in range(size)]

    def draw(self):
        for i, row in enumerate(self.states):
            if i == 0:
                for _ in range(2 * self.size + 3):
                    print("#", end="")
                print()

            print("#", end="")
            for state in row:
                print(" " + state, end="")
            print(" #")

            if i == self.size - 1:
                for _ in range(2 * self.size + 3):
                    print("#", end="")
                print()

    def check_for_end(self):
        # check for win in row
        for i, row in enumerate(self.states):
            result = self.check_states(row)
            if result[0]:
                return result

            # check for win in column
            column = []
            for j in range(self.size):
                column.append(self.states[j][i])
            result = self.check_states(column)
            if result[0]:
                return result

        # check for win in main diagonals
        left_diagonal = []
        for j in range(self.size):
            left_diagonal.append(self.states[j][j])
        result = self.check_states(left_diagonal)
        if result[0]:
            return result

        right_diagonal = []
        for j in range(self.size):
            right_diagonal.append(self.states[j][self.size - j - 1])
        result = self.check_states(right_diagonal)
        if result[0]:
            return result

        # check for win in diagonals under and above the main diagonal (for larger sizes)
        for i in range(1, self.size):
            if self.size - i < 3:
                break

            col = 0
            diagonal_under = []
            diagonal_above = []
            for j in range(i, self.size):
                diagonal_under.append(self.states[j][col])
                diagonal_above.append(self.states[col][j])
                col += 1

            result = self.check_states(diagonal_under)
            if result[0]:
                return result

            result = self.check_states(diagonal_above)
            if result[0]:
                return result

        # check for draw
        for row in self.states:
            if "_" in row:
                return False, None

        return True, None

    @staticmethod
    def check_states(states):
        if 'xxx' in ''.join(state for state in states):
            return True, "x"
        elif 'ooo' in ''.join(state for state in states):
            return True, "o"

        return False, None

    def get_possible_moves(self):
        possible_moves = []
        for i, row in enumerate(self.states):
            for j, state in enumerate(row):
                if state == "_":
                    possible_moves.append((i, j))
        return possible_moves
