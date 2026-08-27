"""Backward compat — delegates to intelligence.features"""
from app.intelligence.features import build_all_features
def build_features(db, entity_type, entity_id): return build_all_features(db, entity_type, entity_id)
