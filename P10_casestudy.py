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
log, event_slots, trails = [], [], []

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

    readiness, energy, stress = predict(readiness, energy, stress, best, steps, last_action)
    last_action = best
    history["readiness"].append(readiness)
    history["energy"].append(energy)
    history["stress"].append(stress)
    log.append((slot, event, best))
    trails.append(best_path)

    if readiness >= GOAL:
        print(f"\nGoal reached at slot {slot}!")
        break

result = "GOAL ACHIEVED" if readiness >= GOAL else "GOAL NOT REACHED"
print("\n" + "=" * 70)
print("AI Decision Summary:", result, f"(final readiness {readiness:.0f}%)")

# ------------------------------------------------------------
# Display: campus grid (left) + state graph (right)
# ------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.5),
                               gridspec_kw={"width_ratios": [1, 1.2]})

# ---- Grid view
for x in range(W):
    for y in range(H):
        ax1.add_patch(Rectangle((x, y), 1, 1, facecolor="white", edgecolor="lightgray"))
for (x, y) in walls:
    ax1.add_patch(Rectangle((x, y), 1, 1, facecolor="#555555", edgecolor="white"))
for name, (x, y) in places.items():
    ax1.add_patch(Rectangle((x, y), 1, 1, facecolor=place_color[name], edgecolor="black"))
    ax1.text(x + 0.5, y + 0.5, name.replace(" ", "\n"), ha="center", va="center",
             fontsize=7, fontweight="bold")
colors = plt.cm.plasma([i / max(1, len(trails)) for i in range(len(trails))])
for i, path in enumerate(trails):
    xs = [p[0] + 0.5 + (i % 3 - 1) * 0.08 for p in path]
    ys = [p[1] + 0.5 + (i % 3 - 1) * 0.08 for p in path]
    ax1.plot(xs, ys, color=colors[i], linewidth=2, alpha=0.7)
    ax1.text(xs[-1], ys[-1] - 0.3, str(i + 1), fontsize=7, color="white",
             ha="center", bbox=dict(boxstyle="circle", facecolor=colors[i], pad=0.15))
ax1.plot(start[0] + 0.5, start[1] + 0.9, "k^", markersize=8)
ax1.plot(pos[0] + 0.5, pos[1] + 0.5, "r*", markersize=18)
ax1.set_xlim(0, W)
ax1.set_ylim(H, 0)
ax1.set_aspect("equal")
ax1.set_xticks(range(W + 1))
ax1.set_yticks(range(H + 1))
ax1.set_title("Campus Grid: Agent's Route (numbers = slot, red star = final position)", fontsize=10)

# ---- Graph view
x = list(range(len(history["readiness"])))
ax2.plot(x, history["readiness"], marker="o", linewidth=2, label="Readiness", color="green")
ax2.plot(x, history["energy"], marker="s", label="Energy", color="orange")
ax2.plot(x, history["stress"], marker="^", label="Stress", color="red")
ax2.axhline(GOAL, linestyle="--", color="gray", label=f"Goal ({GOAL}%)")
for slot, event, action in log:
    ax2.annotate(action, (slot, history["readiness"][slot]), textcoords="offset points",
                 xytext=(0, 8), ha="center", fontsize=6, rotation=45)
for s in event_slots:
    ax2.axvline(s - 0.5, color="purple", alpha=0.25)
ax2.set_xlabel("Study slot")
ax2.set_ylabel("Level (0-100)")
ax2.set_ylim(0, 120)
ax2.legend(loc="upper left", fontsize=8)
ax2.set_title("Readiness, Energy and Stress (purple lines = random events)", fontsize=10)

fig.suptitle("AI EXAM PREP AGENT - Goal-Based Decisions on a Campus Grid",
             fontsize=15, fontweight="bold")
fig.text(0.5, 0.01, "Decision: " + result, ha="center", fontsize=11,
         bbox=dict(boxstyle="round", facecolor="lightgreen"))
plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig("exam_prep_agent_output.png", dpi=150)
plt.show()