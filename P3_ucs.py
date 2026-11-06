from collections import deque
import heapq
import networkx as nx
import matplotlib.pyplot as plt

graph = {
    'A': [('B', 2), ('C', 5)],
    'B': [('D', 4), ('E', 1)],
    'C': [('F', 2)],
    'D': [('G', 3)],
    'E': [('G', 6)],
    'F': [('G', 1)],  # Edge from F to G with cost 1 to match UCS path A -> C -> F -> G (5 + 2 + 1 = 8)
    'G': []
}

start = 'A'
goal = 'G'

def ucs(graph, start, goal):
    priority_queue = [(0, start, [start])]
    visited = set()
    
    while priority_queue:
        cost, current, path = heapq.heappop(priority_queue)
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == goal:
            return path, cost
            
        for neighbor, edge_cost in graph[current]:
            if neighbor not in visited:
                new_cost = cost + edge_cost
                heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))
                
    return None, None

def dfs(graph, start, goal):
    stack = [(start, [start])]
    visited = set()
    
    while stack:
        current, path = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        
        if current == goal:
            return path
            
        for neighbor, cost in reversed(graph[current]):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
                
    return None

def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        if current == goal:
            return path
            
        for neighbor, cost in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
                
    return None

# Compute paths
dfs_path = dfs(graph, start, goal)
bfs_path = bfs(graph, start, goal)
ucs_path, ucs_cost = ucs(graph, start, goal)

# Match exact print format from the observation book
print("Output:")
print("DFS path:", " -> ".join(dfs_path))
print("BFS path:", " -> ".join(bfs_path))
print("UCS path:", " -> ".join(ucs_path))
print("UCS cost:", ucs_cost)

# NetworkX Visualization setup
G = nx.Graph()
for node in graph:
    for neighbor, cost in graph[node]:
        G.add_edge(node, neighbor, weight=cost)

pos = {
    'A': (0, 2), 
    'B': (-2, 1), 
    'C': (2, 1), 
    'D': (-3, 0), 
    'E': (-1, 2), 
    'F': (2, 0), 
    'G': (0, -1)
}

def plot_search(path, title):
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(G, pos, node_size=1800)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20)
    nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
    
    path_edges = list(zip(path, path[:-1])) if path else []
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color='red', arrows=True, arrowsize=25)
    plt.title(title)
    plt.show()

# Display plots
if dfs_path:
    plot_search(dfs_path, "Depth-First Search (DFS)")
if bfs_path:
    plot_search(bfs_path, "Breadth-first Search (BFS)")
if ucs_path:
    plot_search(ucs_path, "Uniform Cost Search (UCS)")