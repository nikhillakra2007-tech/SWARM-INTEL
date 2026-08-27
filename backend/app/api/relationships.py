from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.intelligence.relationships.service import direct_relationships, second_degree

router = APIRouter(prefix="/api", tags=["relationships"])

@router.get("/relationships/{entity_type}/{entity_id}", summary="Direct relationships")
def get_rels(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    try: UUID(entity_id)
    except: raise HTTPException(400, "Invalid UUID")
    rows = direct_relationships(db, entity_type, entity_id)
    return {"entity_type": entity_type, "entity_id": entity_id, "relationships": rows, "count": len(rows)}

@router.get("/network/{entity_type}/{entity_id}", summary="Network expand (2 hops)")
def get_network(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    try: UUID(entity_id)
    except: raise HTTPException(400, "Invalid UUID")
    from app.intelligence.graph.engine import neighbors
    direct = direct_relationships(db, entity_type, entity_id)
    second = second_degree(db, entity_type, entity_id)
    graph = neighbors(db, entity_type, entity_id, depth=2)
    return {"entity_type": entity_type, "entity_id": entity_id, "direct": direct, "second_degree_count": len(second), "graph": graph}
