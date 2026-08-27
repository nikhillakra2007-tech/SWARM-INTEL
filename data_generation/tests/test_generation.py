import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[2]))
sys.path.insert(0, str(pathlib.Path(__file__).parents[2] / "backend"))
from data_generation.config import TARGETS, POPULATION

def test_targets():
    assert TARGETS["customers"] == 10000
    assert TARGETS["relationships"] >= 50000

def test_population():
    assert abs(sum(POPULATION.values()) - 1.0) < 0.01

def test_fraud_scenarios_exist():
    # Check generator defines 10 scenario types
    from data_generation.generator import SCENARIO_TYPES
    assert len(SCENARIO_TYPES) >= 10

def test_reproducibility():
    # Seed check: same seed should give same first customer UUID
    from data_generation.generator import uid
    assert str(uid("CUST_00001")) == str(uid("CUST_00001"))

def test_temporal():
    from datetime import timezone
    from data_generation.config import START_DATE, END_DATE
    import datetime
    assert START_DATE < END_DATE

def test_demo_scenarios():
    from data_generation.generator import generate
    # Light check: generator defines demo refs
    import inspect
    src = inspect.getsource(generate)
    assert "F-9001" in src
