from sqlalchemy import text
from sqlalchemy.orm import Session
import numpy as np

BULK_SQL = text("""
SELECT
  c.customer_id::text as cid,
  c.customer_status,
  (SELECT count(*) FROM loan_applications la WHERE la.customer_id=c.customer_id) as app_cnt,
  (SELECT count(*) FROM customer_device_links cdl WHERE cdl.customer_id=c.customer_id) as dev_cnt,
  (SELECT count(*) FROM entity_relationships er WHERE er.relationship_type='SHARED_DEVICE' AND (er.source_entity_id=c.customer_id OR er.target_entity_id=c.customer_id)) as shared_dev,
  (SELECT count(*) FROM entity_relationships er WHERE er.relationship_type='SHARED_BANK_ACCOUNT' AND (er.source_entity_id=c.customer_id OR er.target_entity_id=c.customer_id)) as shared_bank,
  (SELECT count(*) FROM loan_applications la WHERE la.customer_id=c.customer_id AND la.application_timestamp > now() - interval '7 days') as app_7d,
  COALESCE((SELECT avg(rb.avg_payment_delay_days) FROM repayment_behaviour rb JOIN loans l ON l.loan_id=rb.loan_id JOIN loan_applications la ON la.application_id=l.application_id WHERE la.customer_id=c.customer_id),0) as pay_delay,
  (SELECT count(*) FROM entity_relationships er2 WHERE er2.source_entity_id=c.customer_id OR er2.target_entity_id=c.customer_id) as net_deg
FROM customers c
ORDER BY c.customer_ref
""")

def load_bulk(db: Session):
    rows = db.execute(BULK_SQL).fetchall()
    data=[]
    for r in rows:
        cid, status, app_cnt, dev_cnt, shared_dev, shared_bank, app_7d, pay_delay, net_deg = r
        feats = {
            "network_degree": int(net_deg),
            "application_count": int(app_cnt),
            "device_count": int(dev_cnt),
            "shared_device_count": int(shared_dev),
            "shared_bank_account_count": int(shared_bank),
            "applications_last_7d": int(app_7d),
            "payment_delay_average": float(pay_delay or 0),
        }
        label = 1 if status == "SUSPECT" else 0
        data.append((cid, feats, label))
    return data

def to_arrays(data):
    from model.features.schema import FEATURE_SCHEMA
    X = np.array([[d[1][k] for k in FEATURE_SCHEMA] for d in data], dtype=float)
    y = np.array([d[2] for d in data], dtype=int)
    ids = [d[0] for d in data]
    return X, y, ids
