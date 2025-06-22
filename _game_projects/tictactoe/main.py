# TIC TAC TOE

def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
    print("\n")


def check_winner(board, player):
    # Check each row to see if all cells belong to the current player
    for row in board:
        if row[0] == player and row[1] == player and row[2] == player:
            return True

    # Check each column to see if all cells in a column belong to the current player
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    # Check the top-left to bottom-right diagonal
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    # Check the top-right to bottom-left diagonal
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    # If none of the win conditions are met, return False
    return False


# Check if the game is a draw
def is_draw(board):
    # Loop through every row on the board
    for row in board:
        # Loop through every cell in the row
        for cell in row:
            # If we find an empty space (not "X" or "O"), it's not a draw
            if cell != "X" and cell != "O":
                return False

    # If we didn't find any empty cells, and no one has won, it's a draw
    return True


# Ask for the move from a player
def get_move(player):
    # Keep asking until a valid move is given
    while True:
        # Ask the player for input
        move = input(f"{player}'s move (enter row and column like this: 1 2): ")

        # Try to process the input safely
        try:
            # Remove extra spaces and split the input into two parts
            parts = move.strip().split()

            # Check if there are exactly two parts
            if len(parts) != 2:
                print("Please enter exactly two numbers separated by a space.")
                continue

            # Convert the two parts into integers
            row = int(parts[0])
            col = int(parts[1])

            # Check if both row and column are between 1 and 3
            if row in [1, 2, 3] and col in [1, 2, 3]:
                # Convert to 0-based indexing for our board (Python lists start at 0)
                return row - 1, col - 1
            else:
                print("Invalid numbers! Please use numbers from 1 to 3.")

        # If the conversion to integers fails, handle the error
        except ValueError:
            print("Invalid input! Please enter numbers like: 1 2")



# Entry point of the game
def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)
        row, col = get_move(current_player)

        if board[row][col] != " ":
            print("That spot is already taken. Try again.")
            continue

        board[row][col] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    main()
