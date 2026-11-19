import networkx as nx

G = nx.Graph()
G.add_node("Company A")
G.add_node("Company B")
G.add_node("Tallinn")
G.add_node("Riga")
G.add_edge("Company A", "Tallinn")
G.add_edge("Company B", "Riga")
G.add_edge("Company A", "Company B")

print("Количество вершин:", G.number_of_nodes())
print("Количество ребер:", G.number_of_edges())
print("\nВершины:")
print(list(G.nodes()))
print("\nРебра:")
print(list(G.edges()))
