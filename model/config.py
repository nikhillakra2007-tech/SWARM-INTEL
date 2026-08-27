import pathlib
ROOT = pathlib.Path(__file__).parent
ARTIFACTS = ROOT / "artifacts"
RANDOM_STATE = 42
TEST_SIZE = 0.2
VAL_SIZE = 0.2  # of remaining after test
MODEL_VERSION = "fraud_model_v2"
THRESHOLD = 0.35
FEATURES = [
    "network_degree",
    "application_count",
    "device_count",
    "shared_device_count",
    "shared_bank_account_count",
    "applications_last_7d",
    "payment_delay_average",
]
