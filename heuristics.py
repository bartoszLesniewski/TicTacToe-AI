def calculate_score(row, score, token: str, opponent_token: str):
    str_row = ''.join(state for state in row)
    if token*3 in str_row:
        score += 100
    elif (token*2 + "_" in str_row) or ("_" + token*2 in str_row) or (token + "_" + token in str_row):
        score += 10
    elif (token + "_"*2 in str_row) or ("_"*2 + token in str_row) or ("_" + token + "_" in str_row):
        score += 1
    elif opponent_token*3 in str_row:
        score -= 100
    elif (opponent_token*2 + "_" in str_row) or ("_" + opponent_token*2 in str_row) or (opponent_token + "_" + opponent_token in str_row):
        score -= 10
    elif (opponent_token + "_" * 2 in str_row) or ("_" * 2 + opponent_token in str_row) or ("_" + opponent_token + "_"):
        score -= 1

    # print("Current score: " + str(score))
    return score


def advanced_heuristic(board, token):
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

    for i in range(1, board.size):
        if board.size - i < 3:
            break

        col = 0
        diagonal_under = []
        diagonal_above = []
        for j in range(i, board.size):
            diagonal_under.append(board.states[j][col])
            diagonal_above.append(board.states[col][j])
            col += 1

        score = calculate_score(diagonal_under, score, token, opponent_token)
        score = calculate_score(diagonal_above, score, token, opponent_token)

    print("Score: " + str(score))
    return score


def update_wins_counter(row, x_wins, o_wins):
    str_row = ''.join(state for state in row)

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
        x_wins, o_wins = update_wins_counter(row, x_wins, o_wins)

    # check columns
    for i in range(board.size):
        column = []
        for j in range(board.size):
            column.append(board.states[j][i])

        x_wins, o_wins = update_wins_counter(column, x_wins, o_wins)

    # check main diagonals
    left_diagonal = []
    for j in range(board.size):
        left_diagonal.append(board.states[j][j])

    x_wins, o_wins = update_wins_counter(left_diagonal, x_wins, o_wins)

    right_diagonal = []
    for j in range(board.size):
        right_diagonal.append(board.states[j][board.size - j - 1])

    x_wins, o_wins = update_wins_counter(right_diagonal, x_wins, o_wins)

    # check diagonals under and above the main diagonal (for larger sizes)
    for i in range(1, board.size):
        if board.size - i < 3:
            break

        col = 0
        diagonal_under = []
        diagonal_above = []
        for j in range(i, board.size):
            diagonal_under.append(board.states[j][col])
            diagonal_above.append(board.states[col][j])
            col += 1

        x_wins, o_wins = update_wins_counter(diagonal_under, x_wins, o_wins)
        x_wins, o_wins = update_wins_counter(diagonal_above, x_wins, o_wins)

    if token == "x":
        return x_wins - o_wins
    else:
        return o_wins - x_wins


def update_tokens_with_blanks_counter(x1, x2, o1, o2, token: str, opponent_token: str, row):
    str_row = ''.join(state for state in row)

    if (token + "_" * 2 in str_row) or ("_" * 2 + token in str_row) or ("_" + token + "_" in str_row):
        x1 += 1
    elif (token * 2 + "_" in str_row) or ("_" + token * 2 in str_row) or (token + "_" + token in str_row):
        x2 += 1
    elif (opponent_token * 2 + "_" in str_row) or ("_" + opponent_token * 2 in str_row) or (opponent_token + "_" + opponent_token in str_row):
        o2 += 1
    elif (opponent_token + "_" * 2 in str_row) or ("_" * 2 + opponent_token in str_row) or ("_" + opponent_token + "_"):
        o1 += 1

    return x1, x2, o1, o2


""" 3 * X2 + X1 - (3 * O2 + O1)
Where:
X1 is the number of lines with 1 X and 2 blanks
X2 is the number of lines with 2 X's and a blank
O1 is the number of lines with 1 O and 2 blanks
O2 is the number of lines with 2 O's and a blank """


def extended_heuristic(board, token):
    if token == "x":
        opponent_token = "o"
    else:
        opponent_token = "x"

    x1 = x2 = o1 = o2 = 0

    # check rows
    for row in board.states:
        x1, x2, o1, o2 = update_tokens_with_blanks_counter(x1, x2, o1, o2, token, opponent_token, row)

    # check columns
    for i in range(board.size):
        column = []
        for j in range(board.size):
            column.append(board.states[j][i])

        x1, x2, o1, o2 = update_tokens_with_blanks_counter(x1, x2, o1, o2, token, opponent_token, column)

    # check main diagonals
    left_diagonal = []
    for j in range(board.size):
        left_diagonal.append(board.states[j][j])

    x1, x2, o1, o2 = update_tokens_with_blanks_counter(x1, x2, o1, o2, token, opponent_token, left_diagonal)

    right_diagonal = []
    for j in range(board.size):
        right_diagonal.append(board.states[j][board.size - j - 1])

    x1, x2, o1, o2 = update_tokens_with_blanks_counter(x1, x2, o1, o2, token, opponent_token, right_diagonal)

    # check diagonals under and above the main diagonal (for larger sizes)
    for i in range(1, board.size):
        if board.size - i < 3:
            break

        col = 0
        diagonal_under = []
        diagonal_above = []
        for j in range(i, board.size):
            diagonal_under.append(board.states[j][col])
            diagonal_above.append(board.states[col][j])
            col += 1

        x1, x2, o1, o2 = update_tokens_with_blanks_counter(x1, x2, o1, o2, token, opponent_token, diagonal_under)
        x1, x2, o1, o2 = update_tokens_with_blanks_counter(x1, x2, o1, o2, token, opponent_token, diagonal_above)

    if token == "x":
        return 3 * x2 + x1 - (3 * o2 + o1)
    else:
        return 3 * o2 + o1 - (3 * x2 + x1)
