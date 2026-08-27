from .rules import ALL_RULES

def list_rules(): return [r.__name__ for r in ALL_RULES]
