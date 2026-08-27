def validate(eco):
    errors=[]
    # FKs: check links reference existing ids
    cids={str(c["customer_id"]) for c in eco.customers}
    for l in eco.c_device:
        if str(l["customer_id"]) not in cids:
            errors.append(f"device link bad {l}")
    # counts
    if len(eco.customers) < 5000:
        errors.append("too few customers")
    if len(eco.relationships) < 10000:
        errors.append("too few relationships")
    # fraud ecosystems exist
    if len(eco.clusters) < 5:
        errors.append("no clusters")
    # temporal
    for a in eco.apps:
        if a["application_timestamp"].tzinfo is None:
            errors.append("app missing tz")
    # labels
    for cid, lab in eco.ground_truth.items():
        if lab not in ("normal","suspicious","fraud"):
            errors.append(f"bad label {lab}")
    return errors

def report(eco):
    total=len(eco.customers)
    fraud=sum(1 for v in eco.ground_truth.values() if v=="fraud")
    susp=sum(1 for v in eco.ground_truth.values() if v=="suspicious")
    return {
        "customers": total, "applications": len(eco.apps), "loans": len(eco.loans), "payments": len(eco.payments),
        "devices": len(eco.devices), "mobiles": len(eco.mobiles), "banks": len(eco.banks), "dealers": len(eco.dealers),
        "relationships": len(eco.relationships), "clusters": len(eco.clusters),
        "normal": total-fraud-susp, "suspicious": susp, "fraud": fraud,
        "avg_degree": round(len(eco.relationships)/max(1,total),2),
        "temporal_span": f"{min(a['application_timestamp'] for a in eco.apps).date()} to {max(a['application_timestamp'] for a in eco.apps).date()}" if eco.apps else "n/a"
    }
