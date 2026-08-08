"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x_count += 1
            elif board[i][j] == O:
                o_count += 1

    if x_count > o_count:
        return O
    elif x_count <= o_count:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_move = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_move.add((i,j))
    return possible_move

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = [row[:] for row in board]
    new_board[action[0]][action[1]] = player(board)

    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    winner_position =[
        [(0,0),(0,1),(0,2)],
        [(1,0),(1,1),(1,2)],
        [(2,0),(2,1),(2,2)],
        [(0,0),(1,0),(2,0)],
        [(0,1),(1,1),(2,1)],
        [(0,2),(1,2),(2,2)],
        [(0,0),(1,1),(2,2)],
        [(0,2),(1,1),(2,0)]
    ]

    for posit in winner_position:
        x_count = 0
        o_count = 0
        for j in range(len(posit)):
            if board[posit[j][0]][posit[j][1]] == X:
                x_count += 1
            elif board[posit[j][0]][posit[j][1]] == O:
                o_count += 1
        if x_count == 3:
            return X
        elif o_count == 3:
            return O

    #Outra alternativa para verificar as possibilidades de vitoria
    '''
    for position in winner_position:
        first = board[position[0][0]][position[0][1]]

        if first == EMPTY:
            continue

        if (
            board[position[1][0]][position[1][1]] == first
            and board[position[2][0]][position[2][1]] == first
        ):
            return first 
    '''

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None or actions(board) == set():
        return True

    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    if player(board) == X:
        best_value = -2
        best_action = None

        for action in actions(board):
            value = minimax_value(result(board, action))

            if value > best_value:
                best_value = value
                best_action = action

        return best_action

    else:
        best_value = 2
        best_action = None

        for action in actions(board):
            value = minimax_value(result(board, action))

            if value < best_value:
                best_value = value
                best_action = action

        return best_action

def minimax_value(board):
    if terminal(board):
        return utility(board)

    if player(board) == X:
        return max(
            minimax_value(result(board, action))
            for action in actions(board)
        )

    else:
        return min(
            minimax_value(result(board, action))
            for action in actions(board)
        )
