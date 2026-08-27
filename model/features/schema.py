FEATURE_SCHEMA = [
    "network_degree",
    "application_count",
    "device_count",
    "shared_device_count",
    "shared_bank_account_count",
    "applications_last_7d",
    "payment_delay_average",
]

def validate(features: dict):
    missing = [f for f in FEATURE_SCHEMA if f not in features]
    if missing:
        raise ValueError(f"Missing features: {missing}")
    for f in FEATURE_SCHEMA:
        v = features[f]
        if not isinstance(v, (int, float)):
            raise TypeError(f"Feature {f} must be numeric, got {type(v)}")
    return True
