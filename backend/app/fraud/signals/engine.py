"""Backward compat — delegates to intelligence.rules"""
from app.intelligence.rules.engine import run_rules as analyze_entity, persist as persist_signals
__all__=["analyze_entity","persist_signals"]
