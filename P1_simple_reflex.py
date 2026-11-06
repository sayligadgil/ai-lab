import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

environment = {
    "room1": "clean",
    "room2": "dirty",
    "room3": "clean",
    "room4": "clean"
}

room_positions = {
    "room1": (0, 1),  # top-left
    "room2": (1, 1),  # top-right
    "room3": (0, 0),  # bottom-left
    "room4": (1, 0)   # bottom-right
}

rooms = list(environment.keys())
agent_index = 0

def reflex_agent(state):
    if state == "dirty":
        return "clean"
    else:
        return "move"

def draw_environment(env, agent_pos, step):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Step {step} - Agent in {rooms[agent_pos]}")

    for room, pos in room_positions.items():
        x, y = pos
        color = "red" if env[room] == "dirty" else "green"
        rect = patches.Rectangle(
            (x, y),
            1,
            1,
            facecolor=color,
            edgecolor="black"
        )
        ax.add_patch(rect)
        ax.text(
            x + 0.5,
            y + 0.5,
            room,
            ha="center",
            va="center",
            color="white",
            fontsize=10
        )

    # Draw agent
    agent_x, agent_y = room_positions[rooms[agent_pos]]
    agent_patch = patches.Circle(
        (agent_x + 0.5, agent_y + 0.5),
        0.1,
        color="blue"
    )
    ax.add_patch(agent_patch)
    plt.pause(1)
    plt.close(fig)

plt.ion()
steps = 8
for step in range(steps):
    current_room = rooms[agent_index]
    state = environment[current_room]
    action = reflex_agent(state)
    draw_environment(environment, agent_index, step + 1)

    if action == "clean":
        environment[current_room] = "clean"
    else:
        agent_index = (agent_index + 1) % len(rooms)

plt.ioff()
print("Simulation completed.")
print("Final environment: ", environment)