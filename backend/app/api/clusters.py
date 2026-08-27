from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import FraudCluster, FraudClusterMember

router = APIRouter(prefix="/api/clusters", tags=["clusters"])

@router.get("", summary="List clusters")
def list_clusters(db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100)):
    q = db.query(FraudCluster)
    total = q.count()
    items = q.order_by(FraudCluster.risk_score.desc()).offset((page-1)*size).limit(size).all()
    return {"items": items, "total": total, "page": page, "size": size}

@router.get("/{cluster_id}", summary="Get cluster")
def get_cluster(cluster_id: UUID, db: Session = Depends(get_db)):
    obj = db.query(FraudCluster).filter(FraudCluster.cluster_id==cluster_id).first()
    if not obj: raise HTTPException(404, "Not found")
    return obj

@router.get("/{cluster_id}/members", summary="Cluster members")
def cluster_members(cluster_id: UUID, db: Session = Depends(get_db)):
    if not db.query(FraudCluster).filter(FraudCluster.cluster_id==cluster_id).first():
        raise HTTPException(404, "Cluster not found")
    members = db.query(FraudClusterMember).filter(FraudClusterMember.cluster_id==cluster_id, FraudClusterMember.left_at==None).all()
    return {"cluster_id": cluster_id, "members": members, "count": len(members)}
