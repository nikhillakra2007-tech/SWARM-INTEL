from sqlalchemy.orm import Session
from app.models import EntityRelationship

def direct_relationships(db: Session, entity_type: str, entity_id: str):
    return db.query(EntityRelationship).filter(
        ((EntityRelationship.source_entity_type == entity_type) & (EntityRelationship.source_entity_id == entity_id)) |
        ((EntityRelationship.target_entity_type == entity_type) & (EntityRelationship.target_entity_id == entity_id))
    ).all()

def second_degree(db: Session, entity_type: str, entity_id: str):
    first = direct_relationships(db, entity_type, entity_id)
    # collect neighbor ids
    neighbor_ids = set()
    for r in first:
        if str(r.source_entity_id) == entity_id and r.source_entity_type == entity_type:
            neighbor_ids.add((r.target_entity_type, str(r.target_entity_id)))
        else:
            neighbor_ids.add((r.source_entity_type, str(r.source_entity_id)))
    second = []
    for et, eid in neighbor_ids:
        second.extend(direct_relationships(db, et, eid))
    # exclude original
    return [r for r in second if not ((r.source_entity_type==entity_type and str(r.source_entity_id)==entity_id) or (r.target_entity_type==entity_type and str(r.target_entity_id)==entity_id))]
