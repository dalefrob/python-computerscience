
board = [
    [" "," "," "],
    [" "," "," "],
    [" "," "," "],
]

def checkwinner(player : str):
    for i in range(2):
        # Check for 3 horizontal in a row
        if board[i][0] == player and board[i][1] == player and board[i][2] == player:
             return player
        # Check for 3 vertical in a row
        if board[0][i] == player and board[1][i] == player and board[2][i] == player:
            return player
    # Check for diagonals
    if board[1][1] == player: # If player has the middle -> check corners
        if board[0][0] == player and board[2][2] == player or \
            board[0][2] == player and board[2][0] == player:
                return player
    return None

def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
    print("\n")

current_player = "X"
while True:
    print_board(board)
    try:
        answer = input(f"Player ({current_player}): Pick a position (row col): ") # Ask for input 
        row, col = answer.split(" ")
        row_index = int(row) # Cast to int once
        col_index = int(col)
        if board[row_index][col_index] == " ": # Check if the position is free
            board[row_index][col_index] = current_player # Put X or O in the [row][col] position
        else:
            print("That is already taken - choose again!")
            continue
    except:
        print("Incorrect input.")
        continue

    winner = checkwinner(current_player)
    if winner == current_player:
        print_board(board)
        print(f"{current_player} Wins!")
        break
    
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"
