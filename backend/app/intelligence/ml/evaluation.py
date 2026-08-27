from .training import training_matrix, evaluate
from sqlalchemy.orm import Session

def evaluate_current(db: Session):
    from .model_loader import load_model
    model=load_model()
    if model is None: return {"error": "no model"}
    X,y,_=training_matrix(db)
    return evaluate(model,X,y)
