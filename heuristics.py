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


# (number of lines where X can win) - (number of lines where O can win)
def basic_heuristic(board, token):
    pass

