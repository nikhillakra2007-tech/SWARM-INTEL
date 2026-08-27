from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, confusion_matrix, accuracy_score

def evaluate(y_true, y_prob, threshold=0.5):
    y_pred = (y_prob >= threshold).astype(int)
    try:
        roc = float(roc_auc_score(y_true, y_prob))
    except:
        roc = None
    try:
        pr = float(average_precision_score(y_true, y_prob))
    except:
        pr = None
    cm = confusion_matrix(y_true, y_pred).tolist() if len(set(y_true))>1 else [[len(y_true),0],[0,0]]
    return {
        "threshold": threshold,
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "roc_auc": roc,
        "pr_auc": pr,
        "confusion_matrix": cm,
        "fraud_precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "fraud_recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "fraud_f1": float(f1_score(y_true, y_pred, zero_division=0)),
    }

def choose_threshold(y_true, y_prob):
    # Scan 0.3-0.7 for best F1 respecting recall >=0.7
    best = (0.5, -1)
    for t in [0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7]:
        m = evaluate(y_true, y_prob, threshold=t)
        # prioritize F1 but require recall >=0.5
        score = m["f1"] if m["recall"] >= 0.5 else -1
        if score > best[1]:
            best = (t, score)
    return best[0]
