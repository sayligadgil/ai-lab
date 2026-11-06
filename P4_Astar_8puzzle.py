import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

initial = [
    [2, 8, 3],
    [1, 6, 4],
    [7, 0, 5]
]

goal = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
]

states = [
    [
        [2, 8, 3],
        [1, 6, 4],
        [7, 0, 5]
    ],
    [
        [2, 8, 3],
        [1, 0, 4],
        [7, 6, 5]
    ],
    [
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ]
]

def draw_puzzle(ax, state, title, title_color="skyblue"):
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_aspect("equal")
    ax.axis("off")
    
    ax.add_patch(
        FancyBboxPatch(
            (-0.15, 3.15),
            3.3,
            0.55,
            boxstyle="round, pad=0.05",
            facecolor=title_color,
            edgecolor="none"
        )
    )
    
    ax.text(
        1.5, 3.42,
        title,
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="midnightblue",
    )
    
    for r in range(3):
        for c in range(3):
            value = state[r][c]
            if value == 0:
                cell_color = "lightblue"
            else:
                cell_color = "white"
                
            ax.add_patch(
                Rectangle(
                    (c, 2 - r),
                    1,
                    1,
                    facecolor=cell_color,
                    edgecolor="black",
                    linewidth=2
                )
            )
            
            if value != 0:
                ax.text(
                    c + 0.5,
                    2 - r + 0.5,
                    str(value),
                    ha="center",
                    va="center",
                    fontsize=19,
                    fontweight="bold",
                    color="darkorange",
                )

# Create main figure window
fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor("white")

# Main Title Banner
title_box = FancyBboxPatch(
    (0.18, 0.915),
    0.64,
    0.065,
    boxstyle="round, pad=0.01",
    transform=fig.transFigure,
    facecolor="lightblue",
    edgecolor="none"
)
fig.add_artist(title_box)

fig.text(
    0.5, 0.947,
    "A* Search Algorithm - 8 Puzzle Problem",
    ha="center",
    va="center",
    fontsize=24,
    fontweight="bold",
    color="midnightblue"
)

# Render Initial, Intermediate, and Goal States side-by-side using sub-axes
ax_initial = fig.add_axes([0.10, 0.35, 0.23, 0.40])
draw_puzzle(ax_initial, states[0], "Initial State", "lightsalmon")

ax_mid = fig.add_axes([0.38, 0.35, 0.23, 0.40])
draw_puzzle(ax_mid, states[1], "Intermediate State", "lightyellow")

ax_goal = fig.add_axes([0.66, 0.35, 0.23, 0.40])
draw_puzzle(ax_goal, states[2], "Goal State", "lightgreen")

plt.show()