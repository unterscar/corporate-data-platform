from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
from build_company_graph import get_graph

G = get_graph()

colors = []
for node, data in G.nodes(data=True):
    if data["node_type"] == "company":
        colors.append("skyblue")
    elif data["node_type"] == "city":
        colors.append("lightgreen")
    else:
        colors.append("orange")

positions = nx.spring_layout(G, seed=42)
labels = {node: data["label"] for node, data in G.nodes(data=True)}

plt.figure(figsize=(13, 9))
nx.draw_networkx(G, pos=positions, labels=labels, node_color=colors,
    node_size=1500, font_size=8, edge_color="gray", width=1.5)
plt.title("Граф корпоративной системы")
plt.axis("off")

output_dir = Path("analytics/reports")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = (output_dir / "company_graph.png")

plt.savefig(output_file, dpi=150, bbox_inches="tight")
plt.show()

print("Граф сохранен:", output_file)
