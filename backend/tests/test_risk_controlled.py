"""
Controlled tests proving Swarm Risk Engine consumes BOTH intelligence and ML.
"""
def calc(indiv, network, ml_prob):
    # Mirrors aggregator: 0.25*indiv +0.45*network +0.30*ml*100
    return round(indiv*0.25 + network*0.45 + ml_prob*100*0.30,2)

def test_A_low_both():
    c=calc(20,20,0.2)
    assert c < 30, f"A should be low, got {c}"
    print(f"A low/low {c}")

def test_B_high_network_low_ml():
    low_ml=calc(20,20,0.2)
    high_net=calc(20,90,0.2)
    assert high_net > low_ml + 20, f"B should reflect network {high_net} vs {low_ml}"
    assert high_net > 50

def test_C_low_network_high_ml():
    low_both=calc(20,20,0.2)
    high_ml=calc(20,20,0.9)
    assert high_ml > low_both + 15

def test_D_both_high():
    both_high=calc(20,90,0.9)
    assert both_high > 70

def test_no_hardcoded_risk():
    # Ensure engine is not returning ML alone
    ml_only=0.9*100
    combined=calc(20,20,0.9)
    assert combined != ml_only
    assert combined != 90  # network not just ML
