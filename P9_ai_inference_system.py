import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")

def draw_box(x, y, text, color):
    box = FancyBboxPatch(
        (x, y), 2.5, 1,
        boxstyle="round,pad=0.1",
        facecolor=color, edgecolor="black"
    )
    ax.add_patch(box)
    ax.text(x + 1.25, y + 0.5, text,
            ha="center", va="center", fontsize=10)

draw_box(0.5, 3.5, "Facts\nRavi is a student", "lightblue")
draw_box(3.75, 3.5, "Rule\nStudents study", "lightyellow")
draw_box(7, 3.5, "Conclusion\nRavi studies", "lightgreen")

ax.annotate("", xy=(3.6, 4), xytext=(3.1, 4),
            arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(6.85, 4), xytext=(6.35, 4),
            arrowprops=dict(arrowstyle="->"))

ax.text(5, 2.3, "Query: Does Ravi study?",
        ha="center", fontsize=12)
ax.text(5, 1.5, "Inference Result: TRUE",
        ha="center", fontsize=13, color="green",
        fontweight="bold")

plt.title("AI Inference System")
plt.tight_layout()
plt.show()