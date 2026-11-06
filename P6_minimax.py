import matplotlib.pyplot as plt
import networkx as nx

def minimax(node, depth, is_max, alpha, beta, values):
    if depth == 3:
        return values[node]
        
    if is_max:
        best = float('-inf')
        for i in range(2):
            child = node * 2 + i
            value = minimax(child, depth + 1, False, alpha, beta, values)
            best = max(best, value)
            alpha = max(alpha, best)
            if alpha >= beta:
                print(f"Branch pruned at node {node}")
                break
        return best
    else:
        best = float('inf')
        for i in range(2):
            child = node * 2 + i
            value = minimax(child, depth + 1, True, alpha, beta, values)
            best = min(best, value)
            beta = min(beta, best)
            if alpha >= beta:
                print(f"Branch pruned at node {node}")
                break
        return best

# leaf node values
values = [3, 5, 6, 9, 1, 2, 0, -1]

# Run Minimax
result = minimax(0, 0, True, float('-inf'), float('inf'), values)
print("Optimal value:", result)

G = nx.DiGraph()
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['3', '5'],
    'E': ['6', '9'],
    'F': ['1', '2'],
    'G': ['0', '-1']
}

for parent, children in tree.items():
    for child in children:
        G.add_edge(parent, child)

pos = {
    'A': (0, 3),
    'B': (-2, 2), 'C': (2, 2),
    'D': (-3, 1), 'E': (-1, 1),
    'F': (1, 1), 'G': (3, 1),
    '3': (-3.5, 0), '5': (-2.5, 0),
    '6': (-1.5, 0), '9': (-0.5, 0),
    '1': (0.5, 0), '2': (1.5, 0),
    '0': (2.5, 0), '-1': (3.5, 0)
}

labels = {
    'A': 'MAX', 'B': 'MIN', 'C': 'MIN',
    'D': 'MAX', 'E': 'MAX', 'F': 'MAX', 'G': 'MAX',
    '3': '3', '5': '5', '6': '6', '9': '9',
    '1': '1', '2': '2', '0': '0', '-1': '-1'
}

plt.figure(figsize=(12, 6))
nx.draw(
    G, pos, labels=labels, with_labels=True,
    node_size=1800, node_color='lightblue',
    font_size=11, font_weight='bold', arrows=True
)

plt.title("Minimax Game Tree with Alpha-Beta Pruning")
plt.axis('off')
plt.show()