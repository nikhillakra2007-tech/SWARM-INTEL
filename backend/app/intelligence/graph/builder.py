import networkx as nx
from sqlalchemy.orm import Session
from sqlalchemy import text

_CACHE = {"g": None, "ts": 0}
import time
def build_graph(db: Session, limit: int | None = None) -> nx.Graph:
    if limit is None and _CACHE["g"] is not None and time.time() - _CACHE["ts"] < 10:
        return _CACHE["g"]
    G = nx.Graph()
    q = "SELECT source_entity_type, source_entity_id, target_entity_type, target_entity_id, relationship_type, strength, confidence, evidence_count FROM entity_relationships"
    if limit: q += f" LIMIT {int(limit)}"
    rows = db.execute(text(q)).fetchall()
    for r in rows:
        src = f"{r[0]}:{r[1]}"
        tgt = f"{r[2]}:{r[3]}"
        G.add_node(src, entity_type=r[0], entity_id=str(r[1]))
        G.add_node(tgt, entity_type=r[2], entity_id=str(r[3]))
        G.add_edge(src, tgt, relationship_type=r[4], strength=float(r[5]), confidence=float(r[6]), evidence_count=int(r[7]))
    if limit is None:
        _CACHE["g"] = G
        _CACHE["ts"] = time.time()
    return G

def ego_graph(db: Session, entity_type: str, entity_id: str, depth: int=2) -> nx.Graph:
    from .traversal import bfs_nodes
    G = build_graph(db)
    nodes = bfs_nodes(G, f"{entity_type}:{entity_id}", depth)
    return G.subgraph(nodes).copy() if nodes else nx.Graph()
