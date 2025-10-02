"""
Tic-Tac-Toe with Minimax and Alpha-Beta pruning.
Run: python ttt.py
Controls: Enter positions 1-9 as:
1 2 3
4 5 6
7 8 9
"""
import math
import time

HUMAN = 'O'
AI = 'X'
EMPTY = ' '

def print_board(board):
    print()
    for i in range(3):
        row = [board[3*i + j] if board[3*i + j] != EMPTY else str(3*i + j +1) for j in range(3)]
        print(' ' + ' | '.join(row))
        if i < 2:
            print("---+---+---")
    print()

def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != EMPTY:
            return board[a]
    if EMPTY not in board:
        return 'D'  # draw
    return None

def score(winner, depth):
    if winner == AI:
        return 10 - depth
    elif winner == HUMAN:
        return depth - 10
    else:
        return 0

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner:
        return score(winner, depth), None
    if is_maximizing:
        best = -math.inf
        best_move = None
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                val, _ = minimax(board, depth+1, False)
                board[i] = EMPTY
                if val > best:
                    best = val
                    best_move = i
        return best, best_move
    else:
        best = math.inf
        best_move = None
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                val, _ = minimax(board, depth+1, True)
                board[i] = EMPTY
                if val < best:
                    best = val
                    best_move = i
        return best, best_move

def alphabeta(board, depth, alpha, beta, is_maximizing):
    winner = check_winner(board)
    if winner:
        return score(winner, depth), None
    if is_maximizing:
        best = -math.inf
        best_move = None
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                val, _ = alphabeta(board, depth+1, alpha, beta, False)
                board[i] = EMPTY
                if val > best:
                    best = val
                    best_move = i
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
        return best, best_move
    else:
        best = math.inf
        best_move = None
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                val, _ = alphabeta(board, depth+1, alpha, beta, True)
                board[i] = EMPTY
                if val < best:
                    best = val
                    best_move = i
                beta = min(beta, best)
                if alpha >= beta:
                    break
        return best, best_move

def play():
    board = [EMPTY]*9
    mode = ''
    while mode not in ['1','2']:
        mode = input("Choose mode: 1) Minimax AI as X  2) Alpha-Beta AI as X  : ").strip()
    human_first = ''
    while human_first not in ['y','n']:
        human_first = input("Do you want to go first? (y/n): ").strip().lower()
    human_turn = True if human_first == 'y' else False
    if mode == '1':
        ai_func = minimax
    else:
        ai_func = lambda b,d,mm: alphabeta(b,d,-math.inf,math.inf,mm)
    nodes = {'count':0}
    # We'll track nodes by wrapping the functions if desired. For simplicity, not counting here.
    print_board(board)
    while True:
        if human_turn:
            try:
                move = int(input("Your move (1-9): "))
                if move <1 or move>9 or board[move-1] != EMPTY:
                    print("Invalid move.")
                    continue
                board[move-1] = HUMAN
            except ValueError:
                print("Enter a number 1-9.")
                continue
        else:
            print("AI is thinking...")
            start = time.time()
            _, move = ai_func(board, 0, True)
            duration = time.time() - start
            print(f"AI chooses position {move+1} (took {duration:.4f}s)")
            board[move] = AI
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