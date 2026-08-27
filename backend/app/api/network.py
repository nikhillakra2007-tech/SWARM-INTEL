from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.intelligence.graph.engine import build_graph, connected_components, neighbors
from uuid import UUID
from fastapi import HTTPException

router = APIRouter(prefix="/api/network", tags=["network"])

@router.get("/components", summary="Connected components")
def components(db: Session = Depends(get_db)):
    comps = connected_components(db)
    return {"components": comps, "count": len(comps)}

@router.get("/graph", summary="Full graph stats")
def graph_stats(db: Session = Depends(get_db)):
    G = build_graph(db)
    return {"nodes": G.number_of_nodes(), "edges": G.number_of_edges(), "components": len(list(__import__('networkx').connected_components(G))) if G.number_of_nodes() else 0}
