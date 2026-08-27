from sqlalchemy.orm import Session
from app.intelligence.graph.engine import build_graph
import networkx as nx
import uuid
from app.models import FraudCluster, FraudClusterMember

def detect_clusters(db: Session, min_size: int = 3):
    G = build_graph(db)
    comps = [c for c in nx.connected_components(G) if len(c) >= min_size]
    return comps
