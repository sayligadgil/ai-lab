import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def is_safe(board, row, col):
    for r in range(row):
        if board[r] == col:
            return False
        if abs(board[r] - col) == abs(r - row):
            return False
    return True

def solve(board, row, n):
    if row == n:
        return True

    for col in range(n):
        if is_safe(board, row, col):
            board[row] = col

            if solve(board, row + 1, n):
                return True

            board[row] = -1

    return False

def display_board(board, n):
    chessboard = [
        [(row + col) % 2 for col in range(n)]
        for row in range(n)
    ]

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.imshow(
        chessboard,
        cmap=ListedColormap(["white", "black"]),
        vmin=0, vmax=1
    )

    for row in range(n):
        col = board[row]
        ax.text(
            col, row, "♛",
            ha="center", va="center",
            fontsize=32, color="orange"
        )

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(range(1, n + 1))
    ax.set_yticklabels(range(1, n + 1))

    ax.set_xticks(
        [i - 0.5 for i in range(n + 1)], minor=True
    )
    ax.set_yticks(
        [i - 0.5 for i in range(n + 1)], minor=True
    )

    ax.grid(which="minor", color="gray", linewidth=1.5)
    ax.tick_params(which="minor", bottom=False, left=False)

    ax.set_title("N-Queens Problem")
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")

    plt.tight_layout()
    plt.show()

n = int(input("Enter the number of queens: "))

if n < 1:
    print("Enter a positive number.")
elif n in (2, 3):
    print("No solution exists.")
else:
    board = [-1] * n

    if solve(board, 0, n):
        print("Solution found!")
        print("Queen positions:", [col + 1 for col in board])
        display_board(board, n)
    else:
        print("No solution exists.")