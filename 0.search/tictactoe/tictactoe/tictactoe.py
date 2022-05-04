"""
Tic Tac Toe Player
"""
import math
import copy

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
    num_x, num_o = 0, 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                num_x += 1
            elif board[i][j] == O:
                num_o += 1
    if num_x == num_o:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                all_actions.add((i,j))
    return all_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    tmp_board = copy.deepcopy(board)
    tmp_board[action[0]][action[1]] = player(board)
    return tmp_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]and board[i][0] != EMPTY:
            return board[i][0]
    for j in range(3):
        if board[0][j] == board[1][j]  == board[2][j] and board[0][j] != EMPTY:
            return board[0][j]
    if board[0][0] == board[1][1]  == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1]  == board[2][0] and board[1][1] != EMPTY:
        return board[2][0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True 


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    tmp_winner = winner(board)
    if tmp_winner == X:
        return 1
    elif tmp_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    def max_value(state):
        if terminal(state):
            return (utility(state),None)
        v = -2
        max_acton = None
        for action in actions(state):
            tmp = min_value(result(state, action))
            if tmp[0]> v:
                v = tmp[0]
                max_acton = action
        return (v, max_acton)
    
    def min_value(state):
        if terminal(state):
            return (utility(state),None)
        v = 2
        min_acton = None
        for action in actions(state):
            tmp = max_value(result(state, action))
            if tmp[0] < v:
                v = tmp[0]
                min_acton = action
        return (v, min_acton)
    
    if player(board) == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]
    
