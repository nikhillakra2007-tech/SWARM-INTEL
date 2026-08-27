"""
Targets ~50k lending ecosystem. Adjustable; respects FKs.
"""
SEED = 42
# Targets (approx)
TARGETS = {
    "customers": 10000,
    "devices": 8000,
    "mobiles": 11000,
    "bank_accounts": 9500,
    "addresses": 8500,
    "dealers": 400,
    "guarantors": 5000,
    "ips": 7000,
    "locations": 120,
    "applications": 18000,
    "loans": 11000,
    "payments_per_loan": 4,
    "relationships": 60000,
}
# Population split
POPULATION = {"normal": 0.85, "suspicious": 0.10, "fraud": 0.05}
# Temporal window: 180 days
START_DATE = "2025-03-01"
END_DATE = "2025-08-31"
