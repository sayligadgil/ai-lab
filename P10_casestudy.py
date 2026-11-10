import random
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ------------------------------------------------------------
# GOAL-BASED AI AGENT: EXAM PREP PLANNER ON A CAMPUS GRID
# Goal   : reach 90% exam readiness before the exam
# Grid   : the student agent must WALK to the right place on
#          campus for each activity (travel costs energy)
# Dynamic: energy, stress, random events, closed buildings and
#          blocked paths change every slot, so the agent
#          re-decides (and re-plans its route) every time
# ------------------------------------------------------------

random.seed(1)

GOAL = 90
W, H = 8, 8                        # 8 x 8 grid (columns x rows)
TRAVEL_COST = 0.4                  # energy lost per grid step

# Campus map
walls = {(3, y) for y in range(1, 4)} | {(5, y) for y in range(4, 7)}
places = {
    "Hostel":       (0, 6),
    "Library":      (6, 2),
    "Classroom":    (1, 1),
    "Study Corner": (3, 5),
    "Garden":       (4, 0),
}
symbol = {"Hostel": "H", "Library": "L", "Classroom": "C",
          "Study Corner": "S", "Garden": "G"}
place_color = {"Hostel": "#f9c784", "Library": "#9ecae1", "Classroom": "#c7e9c0",
               "Study Corner": "#dadaeb", "Garden": "#a1d99b"}

# Actions: (readiness gain, energy change, stress change, place to go)
actions = {
    "Study new topics":     (12, -15,  5, "Library"),
    "Practice past papers": (10, -12,  8, "Classroom"),
    "Revise notes":         ( 7,  -8, -2, "Study Corner"),
    "Power nap":            ( 0,  25, -5, "Hostel"),
    "Walk / short break":   ( 0,  12, -15, "Garden"),
}

# Random events: (name, readiness, energy, stress, map effect)
events = [
    ("Power cut at Library",        0,   0,  10, "close:Library"),
    ("Classroom locked",            0,   0,   8, "close:Classroom"),
    ("Construction blocks paths",   0,  -5,   8, "block"),
    ("Friend shared great notes",   8,   0,  -5, None),
    ("Surprise class test",         5, -10,  15, None),
    ("Got a good meal",             0,  12,  -5, None),
    ("Phone distraction",          -4,  -3,   8, None),
]

try:
    slots = int(input("Study slots left before exam (default 12): "))
except ValueError:
    slots = 12

readiness, energy, stress = 20, 70, 30
pos = places["Hostel"]
start = pos
last_action = None


def shortest_path(a, b, blocked):
    """BFS shortest path on the grid, avoiding walls and blocked cells."""
    queue, came = deque([a]), {a: None}
    while queue:
        cur = queue.popleft()
        if cur == b:
            path = []
            while cur is not None:
                path.append(cur)
                cur = came[cur]
            return path[::-1]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (cur[0] + dx, cur[1] + dy)
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in blocked and n not in came:
                came[n] = cur
                queue.append(n)
    return None


def predict(r, e, s, action, dist, last=None):
    """Predict next state if the agent takes an action (incl. travel)."""
    gain, de, ds, _ = actions[action]
    e = max(0, e - TRAVEL_COST * dist)
    efficiency = 0.5 + e / 200               # tired brain learns less
    if action == last:
        efficiency *= 0.7                    # repeating the same thing gets boring
    r = min(100, r + gain * efficiency)
    e = max(0, min(100, e + de))
    s = max(0, min(100, s + ds))
    return r, e, s


def goal_score(r, e, s):
    penalty = max(0, 30 - e) * 2 + max(0, s - 70) * 2
    return r - penalty


def show_grid(pos, path, blocked, closed):
    for y in range(H):
        row = ""
        for x in range(W):
            c = (x, y)
            if c == pos:                          row += " @"
            elif c in walls:                      row += " #"
            elif c in blocked:                    row += " X"
            elif c in places.values():
                name = [k for k, v in places.items() if v == c][0]
                row += " " + (symbol[name].lower() if name == closed else symbol[name])
            elif c in path:                       row += " *"
            else:                                 row += " ."
        print("   " + row)


history = {"readiness": [readiness], "energy": [energy], "stress": [stress]}
log, event_slots, trails, info = [], [], [], []

print("\nGOAL: reach", GOAL, "% readiness")
print("MAP : @ agent | # wall | X blocked path | * route taken | lowercase = closed place")
print("      H Hostel  L Library  C Classroom  S Study Corner  G Garden")
print("=" * 70)

for slot in range(1, slots + 1):
    # 1. Environment changes
    event, closed, blocked = "-", None, set()
    if random.random() < 0.5:
        name, dr, de, ds, effect = random.choice(events)
        readiness = max(0, min(100, readiness + dr))
        energy = max(0, min(100, energy + de))
        stress = max(0, min(100, stress + ds))
        event = name
        event_slots.append(slot)
        if effect and effect.startswith("close:"):
            closed = effect.split(":")[1]
        elif effect == "block":
            free = [(x, y) for x in range(W) for y in range(H)
                    if (x, y) not in walls and (x, y) not in places.values() and (x, y) != pos]
            blocked = set(random.sample(free, 5))

    # 2. Agent evaluates every action: route + predicted outcome
    best, best_val, best_path = None, -1e9, None
    for a, (g, de, ds, place) in actions.items():
        if place == closed:
            continue                              # place is closed right now
        path = shortest_path(pos, places[place], walls | blocked)
        if path is None:
            continue                              # unreachable right now
        val = goal_score(*predict(readiness, energy, stress, a, len(path) - 1, last_action))
        if val > best_val:
            best, best_val, best_path = a, val, path

    # 3. Agent walks the route and performs the action
    steps = len(best_path) - 1
    print(f"\nSLOT {slot} | Event: {event}")
    print(f"State : readiness {readiness:.0f}, energy {energy:.0f}, stress {stress:.0f}")
    print(f"Decision: {best} at {actions[best][3]} ({steps} steps)")
    pos = best_path[-1]
    show_grid(pos, set(best_path), blocked, closed)

    before = (readiness, energy, stress)
    readiness, energy, stress = predict(readiness, energy, stress, best, steps, last_action)
    last_action = best
    history["readiness"].append(readiness)
    history["energy"].append(energy)
    history["stress"].append(stress)
    log.append((slot, event, best))
    trails.append(best_path)
    info.append((event, closed, blocked, best, best_path, before, (readiness, energy, stress)))

    if readiness >= GOAL:
        print(f"\nGoal reached at slot {slot}!")
        break

result = "GOAL ACHIEVED" if readiness >= GOAL else "GOAL NOT REACHED"
print("\n" + "=" * 70)
print("AI Decision Summary:", result, f"(final readiness {readiness:.0f}%)")

# ------------------------------------------------------------
# ANIMATION: watch the agent walk on the 8x8 grid, slot by slot
# ------------------------------------------------------------
from matplotlib.animation import FuncAnimation, PillowWriter

# Build the frames: every walking step, then a pause while the action is done
frames = []
for i, (_, _, _, _, path, _, _) in enumerate(info):
    frames += [(i, k, "walk") for k in range(len(path))]
    frames += [(i, len(path) - 1, "act")] * 3
frames += [(len(info) - 1, len(info[-1][4]) - 1, "done")] * 5

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), gridspec_kw={"width_ratios": [1, 1.2]})


def update(f):
    i, k, phase = frames[f]
    event, closed, blocked, action, path, before, after = info[i]
    ax1.clear()
    ax2.clear()

    # ---- grid
    for x in range(W):
        for y in range(H):
            ax1.add_patch(Rectangle((x, y), 1, 1, facecolor="white", edgecolor="lightgray"))
    for (x, y) in walls:
        ax1.add_patch(Rectangle((x, y), 1, 1, facecolor="#555555", edgecolor="white"))
    for (x, y) in blocked:
        ax1.add_patch(Rectangle((x, y), 1, 1, facecolor="#fdae6b", edgecolor="black"))
        ax1.text(x + 0.5, y + 0.5, "X", ha="center", va="center", fontweight="bold")
    for name, (x, y) in places.items():
        col = "#fb9a99" if name == closed else place_color[name]
        ax1.add_patch(Rectangle((x, y), 1, 1, facecolor=col, edgecolor="black"))
        label = name.replace(" ", "\n") + ("\nCLOSED" if name == closed else "")
        ax1.text(x + 0.5, y + 0.5, label, ha="center", va="center", fontsize=7, fontweight="bold")
    for j in range(i):                                   # earlier routes (faded)
        p = info[j][4]
        ax1.plot([c[0] + 0.5 for c in p], [c[1] + 0.5 for c in p], color="gray", alpha=0.3, linewidth=2)
    walked = path[:k + 1]                                # current route so far
    ax1.plot([c[0] + 0.5 for c in walked], [c[1] + 0.5 for c in walked],
             color="royalblue", linewidth=3, marker=".", markersize=8)
    ax1.plot(path[k][0] + 0.5, path[k][1] + 0.5, "r*", markersize=26, markeredgecolor="black")
    ax1.set_xlim(0, W)
    ax1.set_ylim(H, 0)
    ax1.set_aspect("equal")
    ax1.set_xticks(range(W + 1))
    ax1.set_yticks(range(H + 1))
    ax1.set_title(f"SLOT {i + 1}  |  Event: {event}", fontsize=11, fontweight="bold")
    if phase == "walk":
        status = f"Walking to {actions[action][3]}...  (step {k}/{len(path) - 1})"
    elif phase == "act":
        status = f"Doing: {action}"
    else:
        status = result
    ax1.set_xlabel(status, fontsize=12, fontweight="bold")

    # ---- graph (drawn up to the current slot)
    n = i + (1 if phase != "walk" else 0)
    xs = list(range(n + 1))
    ax2.plot(xs, history["readiness"][:n + 1], marker="o", linewidth=2, label="Readiness", color="green")
    ax2.plot(xs, history["energy"][:n + 1], marker="s", label="Energy", color="orange")
    ax2.plot(xs, history["stress"][:n + 1], marker="^", label="Stress", color="red")
    ax2.axhline(GOAL, linestyle="--", color="gray", label=f"Goal ({GOAL}%)")
    ax2.set_xlim(-0.5, len(info) + 0.5)
    ax2.set_ylim(0, 120)
    ax2.set_xlabel("Study slot")
    ax2.set_ylabel("Level (0-100)")
    ax2.legend(loc="upper left", fontsize=8)
    r_, e_, s_ = after if phase != "walk" else before
    ax2.text(0.98, 0.04, f"Readiness {r_:.0f}%   Energy {e_:.0f}   Stress {s_:.0f}",
             transform=ax2.transAxes, ha="right", fontsize=11,
             bbox=dict(boxstyle="round", facecolor="lightyellow"))
    ax2.set_title("Agent state over time", fontsize=11)


fig.suptitle("AI EXAM PREP AGENT - Goal-Based Movement on 8x8 Campus Grid", fontsize=15, fontweight="bold")
anim = FuncAnimation(fig, update, frames=len(frames), interval=350, repeat=False)

# Save backups (GIF animation + final picture), then play it live
anim.save("exam_prep_agent_animation.gif", writer=PillowWriter(fps=3), dpi=70)
update(len(frames) - 1)
fig.savefig("exam_prep_agent_output.png", dpi=130)
plt.show()
