"""
Connect Four (7x6) with Minimax (with depth limit) and Alpha-Beta pruning.
Run: python connect4.py
Note: Minimax for full-depth Connect Four is expensive; a depth limit is used for reasonable response time.
"""
import math
import time
ROWS = 6
COLS = 7
EMPTY = '.'
HUMAN = 'O'
AI = 'X'

def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print()
    for r in board:
        print('|' + '|'.join(r) + '|')
    print(' ' + ' '.join(map(str, range(1,COLS+1))))
    print()

def is_valid_move(board, col):
    return board[0][col] == EMPTY

def make_move(board, col, piece):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = piece
            return True
    return False

def undo_move(board, col):
    for r in range(ROWS):
        if board[r][col] != EMPTY:
            board[r][col] = EMPTY
            return True
    return False

def check_winner(board):
    # horizontal, vertical, diagonal checks
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] != EMPTY and board[r][c]==board[r][c+1]==board[r][c+2]==board[r][c+3]:
                return board[r][c]
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] != EMPTY and board[r][c]==board[r+1][c]==board[r+2][c]==board[r+3][c]:
                return board[r][c]
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] != EMPTY and board[r][c]==board[r+1][c+1]==board[r+2][c+2]==board[r+3][c+3]:
                return board[r][c]
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] != EMPTY and board[r][c]==board[r-1][c+1]==board[r-2][c+2]==board[r-3][c+3]:
                return board[r][c]
    # draw?
    if all(board[0][c] != EMPTY for c in range(COLS)):
        return 'D'
    return None

def score_window(window, piece):
    opp = HUMAN if piece==AI else AI
    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opp) == 3 and window.count(EMPTY) == 1:
        score -= 4
    return score

def heuristic(board, piece):
    score = 0
    # center column preference
    center_array = [board[r][COLS//2] for r in range(ROWS)]
    score += center_array.count(piece) * 3
    # horizontal
    for r in range(ROWS):
        row_array = board[r]
        for c in range(COLS-3):
            window = row_array[c:c+4]
            score += score_window(window, piece)
    # vertical
    for c in range(COLS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += score_window(window, piece)
    # positive diag
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += score_window(window, piece)
    # negative diag
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += score_window(window, piece)
    return score

def get_valid_locations(board):
    return [c for c in range(COLS) if is_valid_move(board, c)]

def minimax(board, depth, alpha, beta, maximizingPlayer, max_depth):
    winner = check_winner(board)
    if winner == AI:
        return (1000000, None)
    elif winner == HUMAN:
        return (-1000000, None)
    elif winner == 'D':
        return (0, None)
    if depth >= max_depth:
        return (heuristic(board, AI), None)
    valid_locations = get_valid_locations(board)
    if maximizingPlayer:
        value = -math.inf
        column = valid_locations[0]
        for col in valid_locations:
            make_move(board, col, AI)
            new_score, _ = minimax(board, depth+1, alpha, beta, False, max_depth)
            undo_move(board, col)
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, column
    else:
        value = math.inf
        column = valid_locations[0]
        for col in valid_locations:
            make_move(board, col, HUMAN)
            new_score, _ = minimax(board, depth+1, alpha, beta, True, max_depth)
            undo_move(board, col)
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, column

def play():
    board = create_board()
    print("Connect Four - columns 1 to 7")
    print_board(board)
    mode = ''
    while mode not in ['1','2']:
        mode = input("Choose mode: 1) Minimax (depth-limited)  2) Alpha-Beta (with same depth) : ").strip()
    depth = 4
    try:
        d = int(input("Choose search depth (recommended 4-6): "))
        if d>0:
            depth = d
    except:
        pass
    human_first = ''
    while human_first not in ['y','n']:
        human_first = input("Do you want to go first? (y/n): ").strip().lower()
    human_turn = True if human_first == 'y' else False

    while True:
        if human_turn:
            try:
                col = int(input("Your move (1-7): ")) -1
            except:
                print("Enter 1-7")
                continue
            if col<0 or col>=COLS or not is_valid_move(board, col):
                print("Invalid move")
                continue
            make_move(board, col, HUMAN)
        else:
            print("AI is thinking...")
            start = time.time()
            if mode == '1':
                _, col = minimax(board, 0, -math.inf, math.inf, True, depth)
            else:
                _, col = minimax(board, 0, -math.inf, math.inf, True, depth)
            duration = time.time() - start
            print(f"AI chooses column {col+1} (took {duration:.4f}s)")
            make_move(board, col, AI)
        print_board(board)
        winner = check_winner(board)
        if winner:
            if winner == 'D':
                print("It's a draw.")
            else:
                print(f"{winner} wins!")
            break
        human_turn = not human_turn

if __name__ == '__main__':
    play()