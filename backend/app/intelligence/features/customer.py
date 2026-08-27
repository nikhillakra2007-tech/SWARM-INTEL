from sqlalchemy import text
from sqlalchemy.orm import Session

def customer_features(db: Session, customer_id: str) -> dict:
    q = lambda sql: db.execute(text(sql), {"cid": customer_id}).scalar() or 0
    return {
        "application_count": int(q("SELECT count(*) FROM loan_applications WHERE customer_id=:cid")),
        "loan_count": int(q("SELECT count(*) FROM loans l JOIN loan_applications la ON la.application_id=l.application_id WHERE la.customer_id=:cid")),
        "device_count": int(q("SELECT count(*) FROM customer_device_links WHERE customer_id=:cid")),
        "mobile_count": int(q("SELECT count(*) FROM customer_mobile_links WHERE customer_id=:cid")),
        "bank_account_count": int(q("SELECT count(*) FROM customer_bank_links WHERE customer_id=:cid")),
        "address_count": int(q("SELECT count(*) FROM customer_address_links WHERE customer_id=:cid")),
        "dealer_count": int(q("SELECT count(DISTINCT dealer_id) FROM loan_applications WHERE customer_id=:cid AND dealer_id IS NOT NULL")),
        "guarantor_count": int(q("SELECT count(DISTINCT guarantor_id) FROM loan_guarantors lg JOIN loan_applications la ON la.application_id=lg.application_id WHERE la.customer_id=:cid")),
    }
