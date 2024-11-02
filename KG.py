from collections import deque

class Node:
    def __init__(self, id, label):
        self.id = id  
        self.label = label  
        self.properties = {}  

    def add_property(self, key, value):
        self.properties[key] = value

    def __str__(self):
        return f"Node(id={self.id}, label={self.label}, properties={self.properties})"


class Edge:
    def __init__(self, start_node, end_node, label):
        self.start_node = start_node 
        self.end_node = end_node  
        self.label = label  

    def __str__(self):
        return f"Edge(start={self.start_node.id}, end={self.end_node.id}, label={self.label})"


class KnowledgeGraph:
    def __init__(self):
        self.nodes = {}  
        self.edges = []  
        self.indexes = {}  
        self.adjacency_list = {}  

    def add_node(self, id, label):
        if id not in self.nodes:
            self.nodes[id] = Node(id, label)
            self.adjacency_list[id] = []  

    def add_edge(self, start_node_id, end_node_id, label):
        if start_node_id in self.nodes and end_node_id in self.nodes:
            edge = Edge(self.nodes[start_node_id], self.nodes[end_node_id], label)
            self.edges.append(edge)


            self.adjacency_list[start_node_id].append(edge)
            self.adjacency_list[end_node_id].append(edge)

    def add_node_property(self, node_id, key, value):
        if node_id in self.nodes:
            self.nodes[node_id].add_property(key, value)

            if key not in self.indexes:
                self.indexes[key] = {}
            if value not in self.indexes[key]:
                self.indexes[key][value] = []
            self.indexes[key][value].append(node_id)

    def search_nodes_by_property(self, key, value):
        if key in self.indexes and value in self.indexes[key]:
            node_ids = self.indexes[key][value]
            return [self.nodes[node_id] for node_id in node_ids]
        return []

    def search_edges_by_node(self, node_id):
        if node_id in self.adjacency_list:
            return self.adjacency_list[node_id]
        return []

    def find_shortest_path(self, start_node_id, end_node_id):
        if start_node_id not in self.nodes or end_node_id not in self.nodes:
            return None

        queue = deque([(start_node_id, [start_node_id])])
        visited = set()

        while queue:
            current_node, path = queue.popleft()

            if current_node == end_node_id:
                return path

            if current_node not in visited:
                visited.add(current_node)

                for edge in self.adjacency_list[current_node]:
                    neighbor = edge.end_node.id if edge.start_node.id == current_node else edge.start_node.id
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        return None

    def __str__(self):
        nodes_str = "\n".join(str(node) for node in self.nodes.values())
        edges_str = "\n".join(str(edge) for edge in self.edges)
        return f"Nodes:\n{nodes_str}\n\nEdges:\n{edges_str}"

kg = KnowledgeGraph()


with open("dataset.json", "r") as file:
    data = json.load(file)

to_add_nodes = data["nodes"]
for node_data in to_add_nodes:
    kg.add_node(node_data["id"], node_data["label"])
    for key, value in node_data["properties"].items():
        kg.add_node_property(node_data["id"], key, value)

to_add_edges = data["edges"]
for edge_data in to_add_edges:
    kg.add_edge(edge_data["start_node"], edge_data["end_node"], edge_data["label"])

print(kg)


print("Search for nodes with name 'Alice':")
result_nodes = kg.search_nodes_by_property('name', 'Alice')
for node in result_nodes:
    print(node)

print("\nSearch for edges connected to node '1':")
result_edges = kg.search_edges_by_node('1')
for edge in result_edges:
    print(edge)

print("\nFind shortest path between nodes '1' and '4':")
path = kg.find_shortest_path('1', '4')
if path:
    print(" -> ".join(path))
else:
    print("No path found")