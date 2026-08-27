from sklearn.model_selection import train_test_split
import numpy as np

def stratified_split(X, y, test_size=0.2, val_size=0.2, random_state=42):
    # First split test
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    # Then split val from train_val
    # val_size is proportion of train_val that becomes val; convert from overall val_size
    # e.g. overall val 0.2 of total, test 0.2 -> val 0.25 of train_val (since train_val is 0.8)
    val_relative = val_size / (1 - test_size) if (1 - test_size) > 0 else 0.2
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_relative, random_state=random_state, stratify=y_train_val
    )
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)

def time_aware_split_note():
    return "Time-aware split not applied: dataset lacks distinct temporal fraud onset; using stratified random split (seed 42) to preserve 40% fraud rate across splits."
