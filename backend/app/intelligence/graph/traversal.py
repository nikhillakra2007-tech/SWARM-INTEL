import networkx as nx

def bfs_nodes(G: nx.Graph, start: str, depth: int=2) -> set[str]:
    if start not in G: return set()
    visited={start:0}
    queue=[start]
    nodes={start}
    while queue:
        cur=queue.pop(0)
        d=visited[cur]
        if d>=depth: continue
        for nb in G.neighbors(cur):
            if nb not in visited:
                visited[nb]=d+1
                queue.append(nb)
                nodes.add(nb)
    return nodes

def neighbors(db, entity_type: str, entity_id: str, depth: int=1):
    from .builder import build_graph
    G=build_graph(db)
    start=f"{entity_type}:{entity_id}"
    nodes=bfs_nodes(G, start, depth)
    sub=G.subgraph(nodes)
    return {
        "nodes": [{"id": n, **G.nodes[n]} for n in sub.nodes],
        "edges": [{"source": u, "target": v, **d} for u,v,d in sub.edges(data=True)],
        "connected_components": nx.number_connected_components(sub) if len(sub) else 0,
    }
