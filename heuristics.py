# works propoerly only for 3x3 board, for larger sizes always returns 0 or -100
def calculate_score(row, score, token, opponent_token):
    if row.count(token) == 3:
        score += 100
    elif row.count(token) == 2 and row.count("_") == 1:
        score += 10
    elif row.count(token) == 1 and row.count("_") == 2:
        score += 1
    elif row.count(opponent_token) == 3:
        score -= 100
    elif row.count(opponent_token) == 2 and row.count("_") == 1:
        score -= 10
    elif row.count(opponent_token) == 1 and row.count("_") == 2:
        score -= 1

    # print("Current score: " + str(score))
    return score


def heuristic_function(board, token):
    score = 0
    if token == "x":
        opponent_token = "o"
    else:
        opponent_token = "x"

    for row in board.states:
        score = calculate_score(row, score, token, opponent_token)
    for i in range(board.size):
        column = []
        for j in range(board.size):
            column.append(board.states[j][i])
        score = calculate_score(column, score, token, opponent_token)

    diagonal1 = []
    diagonal2 = []
    for i in range(board.size):
        diagonal1.append(board.states[i][i])
        diagonal2.append(board.states[i][board.size - i - 1])

    score = calculate_score(diagonal1, score, token, opponent_token)
    score = calculate_score(diagonal2, score, token, opponent_token)

    return score


def update_wins_counter(str_row, x_wins, o_wins):
    if 'xx_' in str_row or '_xx' in str_row or 'x_x' in str_row:
        x_wins += 1
    elif 'yy_' in str_row or '_yy' in str_row or 'y_y' in str_row:
        o_wins += 1

    return x_wins, o_wins


# (number of lines where X can win) - (number of lines where O can win)
def simple_heuristic(board, token):
    x_wins = 0
    o_wins = 0

    # check rows
    for row in board.states:
        str_row = ''.join(state for state in row)
        x_wins, o_wins = update_wins_counter(str_row, x_wins, o_wins)

    # check columns
    for i in range(board.size):
        column = []
        for j in range(board.size):
            column.append(board.states[j][i])

        str_row = ''.join(state for state in column)
        x_wins, o_wins = update_wins_counter(str_row, x_wins, o_wins)

    # check main diagonals
    left_diagonal = []
    for j in range(board.size):
        left_diagonal.append(board.states[j][j])

    str_row = ''.join(state for state in left_diagonal)
    x_wins, o_wins = update_wins_counter(str_row, x_wins, o_wins)

    right_diagonal = []
    for j in range(board.size):
        right_diagonal.append(board.states[j][board.size - j - 1])

    str_row = ''.join(state for state in right_diagonal)
    x_wins, o_wins = update_wins_counter(str_row, x_wins, o_wins)

    # check diagonals under the main diagonal (for larger sizes)
    for i in range(1, board.size):
        if board.size - i < 3:
            break

        col = 0
        diagonal = []
        for j in range(i, board.size):
            diagonal.append(board.states[j][col])
            col += 1

        str_row = ''.join(state for state in diagonal)
        x_wins, o_wins = update_wins_counter(str_row, x_wins, o_wins)

    # check diagonals above the main diagonal (for larger sizes)
    for i in range(1, board.size):
        if board.size - i < 3:
            break

        col = 0
        diagonal = []
        for j in range(i, board.size):
            diagonal.append(board.states[col][j])
            col += 1

        str_row = ''.join(state for state in diagonal)
        x_wins, o_wins = update_wins_counter(str_row, x_wins, o_wins)

    if token == "x":
        return x_wins - o_wins
    else:
        return o_wins - x_wins
