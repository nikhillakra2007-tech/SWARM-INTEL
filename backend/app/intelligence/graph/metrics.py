import networkx as nx
from sqlalchemy.orm import Session
from .builder import build_graph

def degree(db: Session, entity_type: str, entity_id: str) -> int:
    G=build_graph(db)
    n=f"{entity_type}:{entity_id}"
    return int(G.degree(n)) if n in G else 0

def density_of_ego(db: Session, entity_type: str, entity_id: str, depth: int=1) -> float:
    from .builder import ego_graph
    sub=ego_graph(db, entity_type, entity_id, depth)
    if len(sub)<=1: return 0
    return round(nx.density(sub),4)

def connected_components(db: Session):
    G=build_graph(db)
    comps=list(nx.connected_components(G))
    return [{"size": len(c), "members": list(c)} for c in sorted(comps, key=len, reverse=True)]
