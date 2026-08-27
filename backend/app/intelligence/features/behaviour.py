from sqlalchemy import text
from sqlalchemy.orm import Session

def behaviour_features(db: Session, customer_id: str) -> dict:
    q = lambda sql: db.execute(text(sql), {"cid": customer_id}).scalar() or 0
    app_freq_7d = int(q("SELECT count(*) FROM loan_applications WHERE customer_id=:cid AND application_timestamp > now() - interval '7 days'"))
    pay_delay = db.execute(text("SELECT coalesce(avg(avg_payment_delay_days),0) FROM repayment_behaviour rb JOIN loans l ON l.loan_id=rb.loan_id JOIN loan_applications la ON la.application_id=l.application_id WHERE la.customer_id=:cid"), {"cid": customer_id}).scalar() or 0
    missed = int(q("SELECT coalesce(sum(missed_payment_count),0) FROM repayment_behaviour rb JOIN loans l ON l.loan_id=rb.loan_id JOIN loan_applications la ON la.application_id=l.application_id WHERE la.customer_id=:cid"))
    velocity = db.execute(text("SELECT coalesce(avg(payment_velocity),0) FROM repayment_behaviour rb JOIN loans l ON l.loan_id=rb.loan_id JOIN loan_applications la ON la.application_id=l.application_id WHERE la.customer_id=:cid"), {"cid": customer_id}).scalar() or 0
    device_switch = int(db.execute(text("SELECT count(*) FROM application_events WHERE customer_id=:cid AND event_type='DEVICE_CHANGED'"), {"cid": customer_id}).scalar() or 0)
    loc_change = int(db.execute(text("SELECT count(*) FROM application_events WHERE customer_id=:cid AND event_type='LOCATION_CHANGED'"), {"cid": customer_id}).scalar() or 0)
    return {
        "application_frequency_7d": app_freq_7d,
        "application_burst_rate": round(app_freq_7d/7,3),
        "payment_delay_average": round(float(pay_delay),2),
        "missed_payment_count": int(missed),
        "payment_velocity": round(float(velocity),3),
        "device_switch_frequency": int(device_switch),
        "location_change_frequency": int(loc_change),
    }
