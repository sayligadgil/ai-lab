import matplotlib.pyplot as plt

city_positions = {
    "Hyd": (3, 4),
    "Nalgonda": (2, 2),
    "Warangal": (3, 1),
    "Tirupati": (4, 3),
    "Vijayawada": (5, 2),
    "Kadapa": (5, 5),
    "Nellore": (2, 3),
    "Kurnool": (4, 4)
}

connections = {
    ("Hyd", "Nalgonda"),
    ("Hyd", "Warangal"),
    ("Hyd", "Kurnool"),
    ("Nalgonda", "Vijayawada"),
    ("Kurnool", "Kadapa"),
    ("Kadapa", "Tirupati")
}

plt.figure(figsize=(12, 8))

for c1, c2 in connections:
    x1, y1 = city_positions[c1]
    x2, y2 = city_positions[c2]
    plt.plot([x1, x2], [y1, y2], 'blue', linewidth=2)

path = ["Hyd", "Nalgonda", "Vijayawada"]
for i in range(len(path) - 1):
    c1 = path[i]
    c2 = path[i + 1]
    x1, y1 = city_positions[c1]
    x2, y2 = city_positions[c2]
    plt.plot([x1, x2], [y1, y2], 'red', linewidth=3, linestyle='--')

for city, (x, y) in city_positions.items():
    if city == "Hyd":
        plt.scatter(x, y, s=500, c='Red', edgecolor='Green', zorder=5)
    elif city == "Vijayawada":
        plt.scatter(x, y, s=200, c="red", edgecolor="blue", zorder=5)
    else:
        plt.scatter(x, y, s=200, c="yellow", edgecolor="blue", zorder=5)
    
    plt.text(x + 0.15, y + 0.1, city, fontsize=12, fontweight="bold")

plt.title("STATE-BASED DECISION MAKING AGENT", fontsize=12, fontweight="bold")
plt.text(2.5, 7, "Initial State: Hyd,\nGoal State: Vijayawada", fontsize=14, fontweight="bold")
plt.show()