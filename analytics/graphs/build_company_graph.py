from pathlib import Path
import duckdb
import networkx as nx

data_file = Path("data/raw/companies.csv")

if not data_file.is_file():
    raise FileNotFoundError("Не найден data/raw/companies.csv")

con = duckdb.connect()
companies = con.execute("""
    SELECT id, name, industry, city, employees
    FROM read_csv_auto('data/raw/companies.csv')
""").fetchall()
con.close()

G = nx.Graph()

for company_id, name, industry, city, employees in companies:
    company_node = f"company:{company_id}"
    city_node = f"city:{city}"
    industry_node = f"industry:{industry}"

    G.add_node(
        company_node,
        node_type="company",
        label=name,
        employees=employees
    )

    G.add_node(
        city_node,
        node_type="city",
        label=city
    )

    G.add_node(
        industry_node,
        node_type="industry",
        label=industry
    )

    G.add_edge(company_node, city_node)
    G.add_edge(company_node, industry_node)

print("Количество организаций в CSV:", len(companies))
print("Количество вершин графа:", G.number_of_nodes())
print("Количество рёбер графа:", G.number_of_edges())

print("\nОрганизации:")
for node, data in G.nodes(data=True):
    if data["node_type"] == "company":
        print(data["label"], "-", data["employees"], "сотрудников")

print("\nГорода:")
for node, data in G.nodes(data=True):
    if data["node_type"] == "city":
        print(data["label"])

print("\nОтрасли:")
for node, data in G.nodes(data=True):
    if data["node_type"] == "industry":
        print(data["label"])

company_nodes = [node for node, data in G.nodes(data=True)
    if data["node_type"] == "company"]
if company_nodes:
    selected_company = company_nodes[0]
    print("\nСвязи организации:")
    print(G.nodes[selected_company]["label"])
    for neighbor in G.neighbors(selected_company):
        print("-", G.nodes[neighbor]["label"], "(", G.nodes[neighbor]["node_type"], ")")

print("\nОрганизации по городам:")
for node, data in G.nodes(data=True):
    if data["node_type"] == "city":
        companies_in_city = [G.nodes[neighbor]["label"]
            for neighbor in G.neighbors(node)
            if G.nodes[neighbor]["node_type"] == "company"]
        print(data["label"], ":", ", ".join(companies_in_city))

print("\nОрганизации по отраслям:")
for node, data in G.nodes(data=True):
    if data["node_type"] == "industry":
        organizations = [G.nodes[neighbor]["label"]
            for neighbor in G.neighbors(node)
            if G.nodes[neighbor]["node_type"] == "company"]
        print(data["label"], ":", ", ".join(organizations))

print("\nОбщие города и отрасли:")
for i in range(len(company_nodes)):
    for j in range(i + 1, len(company_nodes)):
        first = company_nodes[i]
        second = company_nodes[j]
        common = (set(G.neighbors(first)) & set(G.neighbors(second)))
        if common:
            print(G.nodes[first]["label"], "<->", G.nodes[second]["label"])
            for node in common:
                print("Общий объект:", G.nodes[node]["label"])

print("\nСтепени вершин:")
for node, degree in G.degree():
    print(G.nodes[node]["label"],  "-", degree)

ranking = sorted(G.degree(), key=lambda item: item[1], reverse=True)
print("\nНаиболее связанные вершины:")
for node, degree in ranking[:5]:
    print(G.nodes[node]["label"], "-", degree)

degree_centrality = nx.degree_centrality(G)
print("\nЦентральность по степени:")
for node, value in sorted(
    degree_centrality.items(),
    key=lambda item: item[1],
    reverse=True)[:5]:
    print(G.nodes[node]["label"], "-", round(value, 3))

betweenness = nx.betweenness_centrality(G)
print("\nПосредническая центральность:")
for node, value in sorted(
    betweenness.items(),
    key=lambda item: item[1],
    reverse=True)[:5]:
    print(G.nodes[node]["label"], "-", round(value, 3))

components = list(nx.connected_components(G))
print("\nКоличество компонент связности:")
print(len(components))
for index, component in enumerate(components, start=1):
    print(f"Компонента {index}:", len(component), "вершин")

if len(company_nodes) >= 2:
    source = company_nodes[0]
    target = company_nodes[1]
    if nx.has_path(G, source, target): 
       path = nx.shortest_path(G, source=source, target=target)
       print("\nКратчайший путь:")
       for node in path:
            print(G.nodes[node]["label"])
    else:
        print("\nМежду выбранными организациями " "нет пути")

def get_graph():
    return G
